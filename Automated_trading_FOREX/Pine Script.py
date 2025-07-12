
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// Srushti_Suresh

//@version=5
i_max_bars_back = 300
indicator(title="ICT Equal Highs and Lows", shorttitle="Equal HL", overlay=true, max_bars_back=i_max_bars_back, max_lines_count=500, max_labels_count=500)

//____________________________ Menu Pivot High Low Start

g_phl_eq = '███████████████ Equal High Low ███████████████'
int i_phl_1_left = input.int(defval=60, title='Left', group=g_phl_eq)
int i_phl_1_right = input.int(defval=30, title='Right', group=g_phl_eq)
tt_eq = "Lower values mean highs and lows are closer."
float i_phl_eq_percent = input.float(defval=0.05, minval=0, step=0.01, title='Equal HL %', tooltip=tt_eq, group=g_phl_eq) 
string i_phl_1_source = input.string(defval='High/Low', title='Source', options=['High/Low', 'Open/Close'], group=g_phl_eq)
color i_phl_1_h_ln_color = input.color(defval=#F7525F, title='Bearish Color', group=g_phl_eq)
color i_phl_1_l_ln_color = input.color(defval=#22AB94, title='Bullish Color', group=g_phl_eq)
int i_phl_eq_transp = input.int(defval=25, minval=0, title='Transparency', group=g_phl_eq) 

//____________________________ Menu Pivot High Low End

//____________________________ Equal High Low Start

// Get Source
float _high = i_phl_1_source == 'Open/Close' ? math.max(open, close) : high
float _low = i_phl_1_source == 'Open/Close' ? math.min(open, close) : low

// Arrays to store the last 2 pivot highs and lows
var float[] ph_arr = array.new_float(2)
var int[] ph_bi_arr = array.new_int(2)
var float[] pl_arr = array.new_float(2)
var int[] pl_bi_arr = array.new_int(2)

// Pivot calculations
int prev_ph_bi = na, int prev_pl_bi = na
bool ph = false, bool pl = false

phl_1_ph = ta.pivothigh(_high, i_phl_1_left, i_phl_1_right)
phl_1_pl = ta.pivotlow(_low, i_phl_1_left, i_phl_1_right)

// Update the arrays with the last 2 pivot highs and lows
if not na(phl_1_ph)
    ph := true
    prev_ph_bi := bar_index - i_phl_1_right
    array.unshift(ph_bi_arr, bar_index)
    array.pop(ph_bi_arr)

if not na(phl_1_pl)
    pl := true
    prev_pl_bi := bar_index - i_phl_1_right
    array.unshift(pl_bi_arr, bar_index)
    array.pop(pl_bi_arr)

// Function to update the arrays with the last 2 values
update_arrays(value, array_ref) =>
    array.unshift(array_ref, value)
    array.pop(array_ref)

// Update arrays with the last 2 pivot highs and lows
if ph
    update_arrays(phl_1_ph, ph_arr)
if pl
    update_arrays(phl_1_pl, pl_arr)

// Get last two pivot highs and lows
ph_price_0 = array.get(ph_arr, 0), ph_price_1 = array.get(ph_arr, 1)
ph_bi_0 = array.get(ph_bi_arr, 0), ph_bi_1 = array.get(ph_bi_arr, 1)

pl_price_0 = array.get(pl_arr, 0), pl_price_1 = array.get(pl_arr, 1)
pl_bi_0 = array.get(pl_bi_arr, 0), pl_bi_1 = array.get(pl_bi_arr, 1)

// Function to calculate percentage change
pchg(price_1, price_2) =>
    change = price_1 - price_2
    percent_change = math.abs((change / price_2) * 100)
    percent_change

// Calculate percentage change between the last two pivot highs and lows
var float ph_pchg = na
var float pl_pchg = na

if array.size(ph_arr) >= 2
    ph_pchg := pchg(array.get(ph_arr, 0), array.get(ph_arr, 1))

if array.size(pl_arr) >= 2
    pl_pchg := pchg(array.get(pl_arr, 0), array.get(pl_arr, 1))

// Draw Equals Box
var levelBoxes_equal = array.new_box()

ph_condition = ph and ph_pchg < i_phl_eq_percent and barstate.isconfirmed
pl_condition = pl and pl_pchg < i_phl_eq_percent and barstate.isconfirmed

if ph_condition
    ph_box = box.new(left=ph_bi_1 - i_phl_1_right, top=ph_price_1, right=ph_bi_0 - i_phl_1_right, bottom=ph_price_0, border_color=color.new(i_phl_1_h_ln_color, i_phl_eq_transp), bgcolor=color.new(i_phl_1_h_ln_color, i_phl_eq_transp))
    array.push(levelBoxes_equal, ph_box)

if pl_condition
    pl_box = box.new(left=pl_bi_1 - i_phl_1_right, top=pl_price_1, right=pl_bi_0 - i_phl_1_right, bottom=pl_price_0, border_color=color.new(i_phl_1_l_ln_color, i_phl_eq_transp), bgcolor=color.new(i_phl_1_l_ln_color, i_phl_eq_transp))
    array.push(levelBoxes_equal, pl_box)

// Plot Equal Labels
plotshape(ph_condition ? high[i_phl_1_right] : na, style=shape.xcross, location=location.absolute, offset=-i_phl_1_right, color=color.new(i_phl_1_h_ln_color, i_phl_eq_transp), size=size.small)
plotshape(pl_condition ? low[i_phl_1_right] : na, style=shape.xcross, location=location.absolute, offset=-i_phl_1_right, color=color.new(i_phl_1_l_ln_color, i_phl_eq_transp), size=size.small)

//____________________________ Equal High Low End

// _____________________________ Code End
