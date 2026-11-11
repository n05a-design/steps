import math

def swing_calc(ppq, bpm, swing_pct):
    span = ppq // 2  # 8th note duration = span for 16th pair
    straight = span // 2
    exact = span * (swing_pct / 100.0)
    quant = round(exact)
    offset = quant - straight
    q_err = quant - exact
    ms_per_tick = (60.0 / bpm / ppq) * 1000.0
    ms_offset = offset * ms_per_tick
    rational_ms_offset = (exact - straight) * ms_per_tick
    ratio = swing_pct / (100.0 - swing_pct)
    return {
        'ppq': ppq, 'bpm': bpm, 'swing_pct': swing_pct,
        'exact_ticks': exact, 'quant_ticks': quant, 'straight_ticks': straight,
        'offset_ticks': offset, 'quant_err': q_err,
        'ms_offset': ms_offset, 'rational_ms_offset': rational_ms_offset,
        'swing_ratio': ratio
    }

for ppq in [480, 960, 240]:
    print(f"=== PPQ {ppq} (BPM 90) ===")
    for s in [50, 54, 55, 58, 60, 61, 62, 66.6667]:
        res = swing_calc(ppq, 90, s)
        print(f"{res['swing_pct']:6.2f}% -> Quant: {res['quant_ticks']:4d} (Exact: {res['exact_ticks']:6.2f}) | Offset: {res['offset_ticks']:+3d} | Delay: {res['ms_offset']:6.2f} ms | Ratio: {res['swing_ratio']:.2f}:1")
