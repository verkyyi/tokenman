"""Ledger append utility for Tokenman's append-only run history."""
from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional, Protocol, TypeAlias, TypedDict

import jsonschema

from harness.git import GitIdentity


class GeneratorBlock(TypedDict):
    prompt_version: str
    output_summary: str
    diff_lines: int
    tokens: int


class EvaluatorBlock(TypedDict):
    prompt_version: str
    verdict: str
    reason: str
    tokens: int


class LedgerEntry(TypedDict):
    run_id: str
    ts: str
    skill: str
    status: str
    pr: Optional[int]
    issue: Optional[int]
    generator: Optional[GeneratorBlock]
    evaluator: Optional[EvaluatorBlock]
    duration_s: int
    total_tokens: int
    verdict: Optional[str]
    verdict_note: Optional[str]


_SCHEMA_PATH = Path(__file__).with_name("ledger.schema.json")


class LedgerInvariantError(ValueError):
    """Raised when a ledger entry violates schema or conditional invariants."""


class LedgerStoreError(RuntimeError):
    """Raised when the backing ledger storage cannot be read or updated."""


class LedgerStore(Protocol):
    def last_run_id(self) -> Optional[int]: ...

    def append(self, entry: LedgerEntry) -> None: ...


LedgerTarget: TypeAlias = Path | LedgerStore


@dataclass(frozen=True)
class StateBranchLedgerStore:
    repo_dir: Path
    branch: str = "tokenman-state"
    remote: str = "origin"
    ledger_relpath: str = "ledger.jsonl"
    identity: GitIdentity = field(
        default_factory=lambda: GitIdentity("tokenman-bot", "tokenman@local")
    )

    def last_run_id(self) -> Optional[int]:
        return _last_run_id_from_lines(self._read_lines())

    def append(self, entry: LedgerEntry) -> None:
        lines = self._read_lines()
        previous = json.loads(lines[-1]) if lines else None
        validate(entry, previous=previous)

        with tempfile.TemporaryDirectory(prefix="tokenman-ledger-") as tmp:
            worktree_dir = Path(tmp) / "state"
            branch_exists = self._sync_branch()
            self._prepare_worktree(worktree_dir=worktree_dir, branch_exists=branch_exists)

            ledger_file = worktree_dir / self.ledger_relpath
            ledger_file.parent.mkdir(parents=True, exist_ok=True)
            with ledger_file.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, separators=(",", ":")) + "\n")

            add = self._run_git(["add", "--", self.ledger_relpath], cwd=worktree_dir)
            if add.returncode != 0:
                raise LedgerStoreError(f"git add failed: {add.stderr.strip()}")

            commit = self._run_git(
                [
                    "-c",
                    f"user.name={self.identity.name}",
                    "-c",
                    f"user.email={self.identity.email}",
                    "commit",
                    "-m",
                    f"[tokenman-ledger] append {entry['run_id']}",
                ],
                cwd=worktree_dir,
            )
            if commit.returncode != 0:
                raise LedgerStoreError(f"git commit failed: {commit.stderr.strip()}")

            push = self._run_git(
                ["push", self.remote, f"HEAD:refs/heads/{self.branch}"],
                cwd=worktree_dir,
            )
            if push.returncode != 0:
                raise LedgerStoreError(f"git push failed: {push.stderr.strip()}")

            self._run_git(
                ["worktree", "remove", "--force", str(worktree_dir)],
                cwd=self.repo_dir,
            )

    def _run_git(
        self,
        args: list[str],
        *,
        cwd: Path,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
        )

    def _local_branch_exists(self) -> bool:
        proc = self._run_git(
            ["rev-parse", "--verify", f"refs/heads/{self.branch}"],
            cwd=self.repo_dir,
        )
        return proc.returncode == 0

    def _remote_branch_exists(self) -> bool:
        proc = self._run_git(
            ["ls-remote", "--exit-code", "--heads", self.remote, self.branch],
            cwd=self.repo_dir,
        )
        if proc.returncode in (0, 2):
            return proc.returncode == 0
        raise LedgerStoreError(f"git ls-remote failed: {proc.stderr.strip()}")

    def _sync_branch(self) -> bool:
        if self._remote_branch_exists():
            fetch = self._run_git(
                ["fetch", self.remote, f"{self.branch}:refs/heads/{self.branch}"],
                cwd=self.repo_dir,
            )
            if fetch.returncode != 0:
                raise LedgerStoreError(f"git fetch failed: {fetch.stderr.strip()}")
            return True
        return self._local_branch_exists()

    def _prepare_worktree(self, *, worktree_dir: Path, branch_exists: bool) -> None:
        if branch_exists:
            add = self._run_git(
                ["worktree", "add", str(worktree_dir), self.branch],
                cwd=self.repo_dir,
            )
            if add.returncode != 0:
                raise LedgerStoreError(
                    f"git worktree add {self.branch} failed: {add.stderr.strip()}"
                )
            return

        add = self._run_git(
            ["worktree", "add", "--detach", str(worktree_dir), "HEAD"],
            cwd=self.repo_dir,
        )
        if add.returncode != 0:
            raise LedgerStoreError(
                f"git worktree add --detach failed: {add.stderr.strip()}"
            )

        orphan = self._run_git(["switch", "--orphan", self.branch], cwd=worktree_dir)
        if orphan.returncode != 0:
            raise LedgerStoreError(
                f"git switch --orphan {self.branch} failed: {orphan.stderr.strip()}"
            )

        rm = self._run_git(["rm", "-rf", "--ignore-unmatch", "--", "."], cwd=worktree_dir)
        if rm.returncode != 0:
            raise LedgerStoreError(f"git rm failed: {rm.stderr.strip()}")

        clean = self._run_git(["clean", "-fdx"], cwd=worktree_dir)
        if clean.returncode != 0:
            raise LedgerStoreError(f"git clean failed: {clean.stderr.strip()}")

    def _read_lines(self) -> list[str]:
        branch_exists = self._sync_branch()
        if not branch_exists:
            return []

        show = self._run_git(
            ["show", f"{self.branch}:{self.ledger_relpath}"],
            cwd=self.repo_dir,
        )
        if show.returncode != 0:
            return []
        return [line for line in show.stdout.splitlines() if line.strip()]


@lru_cache(maxsize=1)
def _load_schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text())


@lru_cache(maxsize=1)
def _schema_validator() -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(_load_schema())


def validate(entry: dict, *, previous: Optional[dict] = None) -> None:
    """Validate entry against the JSON schema and conditional invariants."""
    errors = list(_schema_validator().iter_errors(entry))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise LedgerInvariantError(f"schema: {msgs}")

    status = entry["status"]
    pr = entry.get("pr")
    if status == "pr_opened" and pr is None:
        raise LedgerInvariantError("pr must be non-null when status == 'pr_opened'")
    if status != "pr_opened" and pr is not None:
        raise LedgerInvariantError(
            f"pr must be null when status == {status!r} (got {pr!r})"
        )

    issue = entry.get("issue")
    if status == "issue_opened" and issue is None:
        raise LedgerInvariantError("issue must be non-null when status == 'issue_opened'")
    if status != "issue_opened" and issue is not None:
        raise LedgerInvariantError(
            f"issue must be null when status == {status!r} (got {issue!r})"
        )

    generator = entry.get("generator")
    if status.startswith("skipped_"):
        if generator is not None:
            raise LedgerInvariantError(
                f"generator must be null when status == {status!r}"
            )
    elif status != "error" and generator is None:
        raise LedgerInvariantError(
            f"generator must be populated when status == {status!r}"
        )

    generator_tokens = generator["tokens"] if generator else 0
    evaluator = entry.get("evaluator")
    evaluator_tokens = evaluator["tokens"] if evaluator else 0
    expected = generator_tokens + evaluator_tokens
    if entry["total_tokens"] != expected:
        raise LedgerInvariantError(
            f"total_tokens ({entry['total_tokens']}) != "
            f"generator.tokens ({generator_tokens}) + evaluator.tokens ({evaluator_tokens})"
        )

    if previous is not None:
        previous_run_n = int(previous["run_id"].split("-")[1])
        new_run_n = int(entry["run_id"].split("-")[1])
        if new_run_n <= previous_run_n:
            raise LedgerInvariantError(
                f"run_id {entry['run_id']!r} not strictly greater than previous {previous['run_id']!r}"
            )
        if entry["ts"] < previous["ts"]:
            raise LedgerInvariantError(
                f"ts {entry['ts']!r} is before previous ts {previous['ts']!r}"
            )


def _last_entry(ledger_path: Path) -> Optional[dict]:
    if not ledger_path.is_file():
        return None
    lines = [line for line in ledger_path.read_text().splitlines() if line.strip()]
    if not lines:
        return None
    return json.loads(lines[-1])


def _last_run_id_from_lines(lines: list[str]) -> Optional[int]:
    if not lines:
        return None
    return int(json.loads(lines[-1])["run_id"].split("-")[1])


def last_run_id(target: LedgerTarget) -> Optional[int]:
    if isinstance(target, Path):
        last = _last_entry(target)
        if last is None:
            return None
        return int(last["run_id"].split("-")[1])
    return target.last_run_id()


def append(target: LedgerTarget, entry: LedgerEntry) -> None:
    if not isinstance(target, Path):
        target.append(entry)
        return

    ledger_path = target
    previous = _last_entry(ledger_path)
    validate(entry, previous=previous)

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, separators=(",", ":")) + "\n")
