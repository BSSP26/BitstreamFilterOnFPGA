## HDL Design

Target platform: Digilent Cmod A7-35T (Xilinx XC7A35T).  
System clock: 12 MHz (onboard oscillator).  
Tools: Vivado 2022.2.

### Build

Open Vivado, create a new project and select the Digilent Cmod A7-35T 
board (digilentinc.com:cmod_a7-35t:part0:1.1). Add all files from hdl/ 
and constraints/, set TOP as the top module, and run synthesis, 
implementation, and bitstream generation.

Expected utilization: approximately 470-520 LUTs for the filter, 
0 DSP blocks, depending on synthesis settings. The complete synthesized 
design additionally includes a LFSR excitation source 
(20 LUTs), which serves as a built-in test signal and is not part of 
the filter itself.

These resources are lower than the 566 LUTs reported in Table II of the 
paper, because the static AE wrapper drives the filter parameters with 
compile-time localparams instead of runtime-configurable inputs.

### Measurement Configurations

The bitstream filter exposes cutoff (alpha), resonance, and input gain as runtime-capable
parameter inputs. In `TOP.v`, these inputs are driven by compile-time
`localparam` values to provide reproducible static AE builds. The default
configuration corresponds to Fig. 10 @TAP_4. To reproduce other figures, modify
the parameters and re-synthesize.

Constants from Table I of the paper:  
fs = 12 MHz, k = 19098593, fres = 0.1 Hz.  
Cutoff: alpha = fc × 10.  
Resonance: effective g = RESONANCE_GAIN × 4 / 127.

| Figure | ALPHA | RESONANCE_GAIN | INPUT_GAIN | Output |
|--------|-------|----------------|------------|--------|
| Fig. 9 left | 200000 | 0 | 127 | TAP_4 |
| Fig. 9 right | 200000 | 127 | 2 | TAP_4 |
| Fig. 10 | 4400 | 0 | 127 | TAP_1..TAP_4 (separate builds) |
| Fig. 11 | 1100, 2200, 4400, 8800, 17600, 35200, 70400, 140800 | 0 | 127 | TAP_4 |
| Fig. 12 | 4400 | 0, 32, 64, 96, 112, 120, 127 | 127 | TAP_4 |

For Fig. 10, the four pole taps are observed in separate builds: 
modify the BITSTREAM_FILTER instantiation in TOP.v to route the desired tap to 
FILTER_OUT.

Fig. 9 right (self-oscillation at g = 4) in the paper was measured 
with the full runtime-controlled setup, where the filter loop was 
first excited and the input was then removed. With the static wrapper, 
self-oscillation can be reproduced by setting ALPHA = 200000, 
RESONANCE_GAIN = 127, INPUT_GAIN = 2. The minimal constant input 
(INPUT_GAIN = 2) lets the loop ramp up into oscillation while 
remaining negligible in the spectrum. The result is close to, but 
not bit-identical with, the paper measurement.

## Hardware Measurement Setup

The measurement chain corresponds to Fig. 8 in the paper:

- **PMOD_DIRECT_STREAM** (Pmod JA pin 1 / G17): 1-bit bitstream output 
  routed to a Keysight N9322C spectrum analyzer through a 1 kΩ series 
  resistor for full-band measurements.
- **FILTER_OUT** (V8): On the carrier board, this pin is 
  connected to an analog low-pass filter (60 kHz cutoff) followed by a 
  24-bit audio interface at 192 kHz. Audio-band measurements use a 
  65536-point FFT with Hann window and 60 s averaging.

## Reproducing the Paper Figures

### Python environment
Required: numpy, matplotlib, pandas.  
Tested with Python 3.10.11.

### Simulations (Fig. 3)
The analytical and sample-by-sample simulation data/scripts for Fig. 3 are
provided under `simulation/fig3_noise_shaping/`.

### Hardware measurements (Fig. 9-12)
Each subfolder under `measurements/` contains the raw spectrum analyzer 
or audio interface CSV files together with a Python script that 
generates the corresponding paper figure.

## THD Calculation

The CSV contains the audio-band spectrum of the self-oscillating 
filter at fc = 440 Hz, g = 4.

THD was computed from the peak magnitudes of the first ten harmonics 
(H1 to H10) using:

THD [%] = 100 * sqrt(sum(P_n, n=2..N)) / sqrt(sum(P_n, n=1..N))

where P_n denotes the power of the n-th harmonic.

Result: 0.35%.

## License

The HDL design files in `hdl/` are licensed under CERN-OHL-S-2.0.

The Python scripts in `measurements/` and `simulation/` are licensed under the MIT License.

The measurement data are provided as part of this artifact for reproducibility.

See `LICENSE` for details.
