"""Physical and mathematical constants, declared once.

物理与数学常量，只声明一次。

These are not configuration: nothing here is a judgement call, so nothing here is
overridable.  They are declared in one place because the same conversion had been
spelled several ways — the σ→FWHM factor as `2.35482` (truncated) in the fitting
tools, `2.355` (rounded) in `utils/VI.py`, and `2·√(2·ln 2)` (exact) in the CWT
finder; and the speed of light as `2.99792458e5` in the fitting tools and the
outflow rule but `3e5` in the CWT catalog's `FWHM_km_s` column.

这些不是配置：这里没有任何需要判断的选择，因此也没有任何可覆盖项。它们集中声明，是因为同一个换算
此前被写成几种形式——σ→FWHM 系数在拟合工具里是 `2.35482`（截断）、在 `utils/VI.py` 里是
`2.355`（四舍五入）、在 CWT 找特征里是 `2·√(2·ln 2)`（精确）；光速在拟合工具与外流规则里是
`2.99792458e5`，而 CWT 目录的 `FWHM_km_s` 列用的是 `3e5`。

The 0.069 % difference between the two speeds of light is enough to flip a declared
width band near a boundary: a feature whose true width is 999.5 km/s becomes 1000.4
with `3e5` (band `intermediate`) but 999.2 with the exact value (band `narrow`), so
the label depended on which producer computed the number.
两个光速取值相差 0.069 %，足以在边界附近翻转已声明的宽度档：真实宽度 999.5 km/s 的特征用
`3e5` 算得 1000.4（`intermediate` 档），用精确值算得 999.2（`narrow` 档），因此标签曾取决于
哪个生产者算了这个数。
"""

from __future__ import annotations

import math

#: Speed of light in vacuum, km/s (exact SI value) / 真空光速，km/s（精确 SI 值）。
SPEED_OF_LIGHT_KMS = 2.99792458e5

#: Gaussian FWHM per unit sigma, ``2·√(2·ln 2)`` — computed, never rounded.
#: 高斯 FWHM 与 σ 之比，``2·√(2·ln 2)``——现算，不取整。
SIGMA_TO_FWHM = 2.0 * math.sqrt(2.0 * math.log(2.0))

#: The inverse conversion, so no caller divides by a literal.
#: 反向换算，使调用方无需除以字面量。
FWHM_TO_SIGMA = 1.0 / SIGMA_TO_FWHM
