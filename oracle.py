# Henry Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

L = "each inductance must be from 0.01 to 100000 µH with at most two decimal places"
I = "the current must be from 0.01 to 1000 A with at most two decimal places"

def p(t, err, intdigits, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or len(parts[0]) > intdigits or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v):
    s, f = str(v // 100), str(v % 100).rjust(2, "0").rstrip("0")
    return s + "." + f if f else s

def uh(x): return dec(x) + " µH"
def aa(x): return dec(x) + " A"
def uwb(l100, i100): return dec(int(hu(Fraction(l100) * i100, 100))) + " µWb"
def mjx(l100, i100): return int(hu(Fraction(l100) * i100 * i100, 20000000))
def mj(l100, i100): return dec(mjx(l100, i100)) + " mJ"

def inn(l1, l2, i):
    out = {"a": p(l1, L, 6, 1, 10000000)}
    if l2 is not None: out["b"] = p(l2, L, 6, 1, 10000000)
    if i is not None: out["i"] = p(i, I, 4, 1, 100000)
    return out

def energyTruth(ind, amps):
    x = inn(ind, None, amps)
    return "A " + uh(x["a"]) + " inductor carrying " + aa(x["i"]) + " links " + uwb(x["a"], x["i"]) + " of flux and stores " + mj(x["a"], x["i"]) + " of energy."

def seriesTruth(l1, l2, amps):
    x = inn(l1, l2, amps); s = x["a"] + x["b"]
    e1 = int(hu(Fraction(mjx(s, x["i"])) * x["a"], s)); e2 = int(hu(Fraction(mjx(s, x["i"])) * x["b"], s))
    return uh(x["a"]) + " and " + uh(x["b"]) + " in series act like " + uh(s) + ". At " + aa(x["i"]) + " the pair stores " + mj(s, x["i"]) + ", with " + dec(e1) + " mJ in the " + uh(x["a"]) + " one and " + dec(e2) + " mJ in the " + uh(x["b"]) + " one."

def parallelTruth(l1, l2, amps):
    x = inn(l1, l2, amps); s = x["a"] + x["b"]
    eq = int(hu(Fraction(x["a"]) * x["b"], s))
    i1 = int(hu(Fraction(x["i"]) * x["b"], s)); i2 = int(hu(Fraction(x["i"]) * x["a"], s))
    return uh(x["a"]) + " and " + uh(x["b"]) + " in parallel act like " + uh(eq) + ". A " + aa(x["i"]) + " total splits into " + aa(i1) + " in the " + uh(x["a"]) + " one and " + aa(i2) + " in the " + uh(x["b"]) + " one."

FNS = {"energyTruth": energyTruth, "seriesTruth": seriesTruth, "parallelTruth": parallelTruth}

cases = []
ls = ["0.01", "4.7", "100", "47", "100000"]
for l in ls:
    for i in ["0.01", "0.5", "2", "999.99", "1000"]:
        cases.append(("energyTruth", [l, i]))
for l1 in ["0.01", "100", "47", "100000"]:
    for l2 in ["0.01", "47", "100000"]:
        for i in ["0.01", "2", "1000"]:
            cases.append(("seriesTruth", [l1, l2, i]))
            cases.append(("parallelTruth", [l1, l2, i]))
errs = ["0", "100001", "1.5", "x", ""]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for bad in errs:
    for name, args in [("energyTruth", [bad, "2"]), ("energyTruth", ["100", bad]),
                       ("seriesTruth", [bad, "47", "2"]), ("seriesTruth", ["100", bad, "2"]),
                       ("seriesTruth", ["100", "47", bad]), ("parallelTruth", [bad, "47", "2"]),
                       ("parallelTruth", ["100", "47", bad])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
