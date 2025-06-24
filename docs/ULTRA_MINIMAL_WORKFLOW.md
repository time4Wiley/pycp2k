# Ultra-Minimal Workflow — M1 Pro ⇄ HPC Cheatsheet

Last updated: commit after laptop debugging session (M1 Pro, CP2K 2025.1-Homebrew)

---

## 1  Environment Matrix

| Target | Executable | MPI | Notes |
|--------|------------|-----|-------|
| **Laptop (M1 Pro)** | `cp2k.ssmp` | ❌ | Serial / OpenMP only |
| **HPC** | `cp2k.psmp` | ✅ | MPI + OpenMP |

Keep batch/job scripts in `cp2k_computation` aligned with the target.

---

## 2  pycp2k Schema Pitfalls (fixed)

| Broken attempt | Working fix |
|----------------|-------------|
| `SCF.Guess` / `SCF.GUESS` | *Remove* — pycp2k doesn't expose a GUESS keyword; CP2K falls back automatically |
| `motion.PRINT.TRAJECTORY` direct access | `motion.PRINT_add().TRAJECTORY` |
| `EACH.GEO_OPT` / `EACH.MD` | Not in schema ⇒ omit trajectory printing for ultra-minimal jobs |
| `TRAJECTORY.FILENAME` | Not exposed ⇒ omit |

---

## 3  Basis-Set Corrections

```text
B  : SZV-MOLOPT-SR-GTH   + GTH-PBE-q3
Ti : SZV-MOLOPT-SR-GTH   + GTH-PBE-q12
```
(The default `SZV-MOLOPT-GTH` does **not** exist for Boron.)

---

## 4  build_ultraminimal_test.py

* Generates six inputs (`ultramin_*_{geo,md}.inp`) sized 5-9 atoms.
* No trajectory prints, no SCF guess.

Files now compile without schema errors.

---

## 5  Laptop Timing (serial `cp2k.ssmp`)

```
5-atom Ti3C2 surface   ≈ 30 s / SCF step
8-atom combined        ≈ 1 m 45 s / SCF step
9-atom boronate-diol   ≈ 2 m 20 s / SCF step
```
Geo-opt ≤ 50 steps → 10-50 min; acceptable on laptop.

---

## 6  HPC Hints

* Switch executable back to `cp2k.psmp` in batch scripts.
* If you need trajectory printing, append raw text manually after generation:

```text
&PRINT
  &TRAJECTORY
    &EACH
      MD 10
    &END
  &END
&END
```
(Faster than fighting the pycp2k schema.)

---

## 7  Relevant Commits

1. **Verify local CP2K 2025.1 installation on M1 Pro** – adds verification tests.
2. **Fix build_ultraminimal_test.py** – basis-set + schema fixes; inputs now build.

---

*Drop this file in any future Cursor session to avoid re-solving the same issues.* 