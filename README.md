# Henry Math

Inductor arithmetic. A 100 µH inductor carrying 2 A links 200 µWb of flux and stores 0.2 mJ. Two in parallel act like 31.97 µH and split the current in inverse proportion.

## What it computes

- **The energy truth** - flux linkage (µWb) and stored energy (mJ) for one inductor (0.01 to 100000 µH) at a current (0.01 to 1000 A).
- **The series truth** - two inductors in series add up, and the stored energy splits in proportion.
- **The parallel truth** - two inductors in parallel shrink like a product over a sum, and the current splits in inverse proportion.

## Boundary

Arithmetic only. The inductances and currents are the owner's own entries, every inductor treated as ideal. It has not seen any circuit and does not know the core, saturation, resistance, heat or insulation, and it gives no verdict that an inductor, a winding or a supply is adequate or safe. A charged inductor can bite when its circuit opens. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a µH and hundredths of an A, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/henrymath/
Repo: https://github.com/iLanis-agent/henrymath
