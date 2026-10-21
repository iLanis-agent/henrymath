// Henry Math engine: energy and flux on one inductor, two in series, two in parallel with the current split. Exact integers (hundredths of a uH, hundredths of an A), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _L = "each inductance must be from 0.01 to 100000 µH with at most two decimal places";
var _I = "the current must be from 0.01 to 1000 A with at most two decimal places";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _uh(l) { return _dec(l, 2) + " µH"; }
function _a(i) { return _dec(i, 2) + " A"; }
function _uwb(l100, i100) { return _dec(_hu(l100 * i100, 100), 2) + " µWb"; } // hundredths of a µWb
function _mj(l100, i100) { return _dec(_hu(l100 * i100 * i100, 20000000), 2) + " mJ"; } // hundredths of a mJ
function _mjx(l100, i100) { return _hu(l100 * i100 * i100, 20000000); } // numeric hundredths of a mJ
function _in(l1, l2, i) {
  var out = { a: _p(l1, _L, 6, 2, 1, 10000000) };
  if (l2 !== undefined) out.b = _p(l2, _L, 6, 2, 1, 10000000);
  if (i !== undefined) out.i = _p(i, _I, 4, 2, 1, 100000);
  return out;
}

function energyTruth(ind, amps) {
  var p = _in(ind, undefined, amps);
  return "A " + _uh(p.a) + " inductor carrying " + _a(p.i) + " links " + _uwb(p.a, p.i) + " of flux and stores " + _mj(p.a, p.i) + " of energy.";
}
function seriesTruth(l1, l2, amps) {
  var p = _in(l1, l2, amps), s = p.a + p.b;
  var e1n = _hu(_mjx(s, p.i) * p.a, s), e2n = _hu(_mjx(s, p.i) * p.b, s);
  return _uh(p.a) + " and " + _uh(p.b) + " in series act like " + _uh(s) + ". At " + _a(p.i) + " the pair stores " + _mj(s, p.i) + ", with " + _dec(e1n, 2) + " mJ in the " + _uh(p.a) + " one and " + _dec(e2n, 2) + " mJ in the " + _uh(p.b) + " one.";
}
function parallelTruth(l1, l2, amps) {
  var p = _in(l1, l2, amps), s = p.a + p.b;
  var eq = _hu(p.a * p.b, s); // display only
  var i1 = _hu(p.i * p.b, s), i2 = _hu(p.i * p.a, s);
  return _uh(p.a) + " and " + _uh(p.b) + " in parallel act like " + _uh(eq) + ". A " + _a(p.i) + " total splits into " + _a(i1) + " in the " + _uh(p.a) + " one and " + _a(i2) + " in the " + _uh(p.b) + " one.";
}
