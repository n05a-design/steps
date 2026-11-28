# Windows shell resource integrity handoff

**Owner disposition pending.** At the V2.1 verification base, all 23 SHA-256 entries in the shell manifest match the exact Git blobs. With Windows `core.autocrlf=true`, the same 23 entries were materialized with different bytes. Git assigns `text=auto` and no explicit `eol`. The wheel copied the working-copy bytes, and the installer preserved those wheel bytes. The per-path hashes and attributes for each checkout, wheel entry and installed copy are in the local `v22-shell-byte-comparison.json` artifact.

Example `glide_shell/AI_GUIDE_NEW_PROJECTS.md` has manifest and Git blob SHA-256 `266115044d2546a9ec9d946b1f38aae3213bb87a1b4da8dbe24565ae87439a29`. Its CRLF working copy, packaged copy and installed copy each hash to `719c0ccc5fb5a8e4bfc413d292fdf27fb4d92b2667f7c065cbc3218d71bb1e19`. The LF wheel and install match the manifest.

| Candidate | Integrity implications | Owner validation |
| --- | --- | --- |
| Path-scoped `text eol=lf` for imported text | Stable LF materialization under normal Windows and POSIX checkout. Scope must track the manifest and avoid binary resources. | Check a fresh Windows checkout with AutoCRLF enabled, tracked blob change count, upstream source hashes and a fresh wheel. |
| Path-scoped `-text` for all imported resources | Git preserves exact bytes of imported resources and editor changes could still drift. Validate any new resource against the import contract. | Repeat source-to-blob, checkout-to-wheel and wheel-to-install tests on all manifest entries. |
| Explicit normalization in manifest checks | Changes the verification contract by treating bytes with distinct line endings as equal. Requires updated upstream/import policy and handling for binary files. | Document a versioned validation contract and test missing, altered and incorrectly normalized files. Preserve exact source provenance separately. |

Run `git ls-files --eol glide_shell`, `git check-attr text eol -- glide_shell/AI_GUIDE_NEW_PROJECTS.md`, and `python -B -m unittest tests.test_glide_shell_integration tests.test_package_artifacts -v` in both checkouts. The failing checks are shell self-test, manifest isolation and installed wheel smoke. The MVVE branch preserves the failure and leaves all shell sources, attributes and rules unchanged. [Shell manifest](../../../glide_shell/SHELL_MANIFEST.json)
