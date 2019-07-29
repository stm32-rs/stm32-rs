# Changelog

## [Unreleased]

## [v0.8.0] 2019-07-28

Family-specific:
* F1:
    * FLASH ACR LATENCY field (#221)
    * ADC definitions (#233)
    * BKP definitions (#235, #256)
    * RTC definitions (#237)
    * Fix PLLMUL confusion (#259)
* F2:
    * ETH definitions (#252)
* F4:
    * F469: Renamed 48MSEL to CK48MSEL to avoid leading numerals (#199)
    * F411: Fixed missing interrupts (#268)
    * OTG HS peripheral fixes (#230)
* L0: Renamed 1_8V constants to V1_8 (etc) to avoid leading numerals (#199)
* L4:
    * Add nBOOT0 and nSWBOOT0 to FLASH OPTR (#217);w
    * L4x2: Document USB registers (#195)
    * L4x3: Add missing CRCCR register (#219)
    * L4x5: Fix wrong RNG interrupt value (#268)
* G0:
    * Renamed devices to STM32G0x0 and STM32G0x1 (#200)
    * DMA patch (#228)
* G4:
    * Initial support (#229)
* H7:
    * Fix width of ETHERNET_DMA.DMAMR.INTM (#201)
    * Fix DMA SC?R and cluster streams (#202)
    * Document DMAMUX{1,2} and split flag fields (#203)
    * Add missing DBGMCU (#204)
    * Fix CFG.FTHV/L spelling (#205)
    * RCC definitions and patches (#206, #242)
    * Update SVD file to ST version 1.4 (#208)
    * Fix MTLTxQUR and PPSCTRL (#211)
    * SPI DXPIE/TXPIE set to read-write (#215)
    * Fix Flash register access and RCC USART/UART field names (#218)
    * ADC definitions and fixes (#231, #244, #264)
    * LPTIM definitions (#240)
    * RNG definitions (#246)
    * Split into four devices: H743/H743v/H753/H753v (#247)

Common:
* Updated svdpatch.py to prohibit enumerated values with leading numerals
  (#199)
* PAR register added to DMA cluster on many families (#214)
* NotHalt renamed to NotHalf for DMA HTIF fields (#216)
* Timers:
    * TIM1 and CKD descriptions (#220)
    * TIM CCMR (#223)
    * TIM3/4 16-bit and definitions (#241)
    * Advanced timer definitions (#267)
* DAC refactor (#234)
* SAI definitions (#249)
* FMC/FSMC definitions (#253, #265)
* CAN definitoins (#254)
* DMA and LPTIM enums updated to new numeric format (#262)
* `async` in ADC renamed `asynchronous` since it's a keyword now (#263)

Thanks to:

[@nickray] [@jordens] [@richardeoin] [@mabezdev] [@burrbull] [@dotcypress]
[@albru123]

## [v0.7.0] 2019-04-22

Family-specific:
* F0: Add missing DMA interrupts (#181), flash peripheral (#172)
* F1: Add enumerated values for GPIO (#186)
* F3: Split up and fix `SYSCFG`, `COMP`, and `OPAMP` (#173, #189)
* F4: Missing USART interrupts added for F401 (#144)
* F7: Add some FMC documentation (#20)
* L0: Extensive updates (#148, #161) to L0 family coverage
* L4: Add RCC CRRCR register (#141), rename RCC APB1ENR1.SP3EN to SPI3EN (#183)
* H7: SPI CSTART update (#179), DMA and DMAMUX updates (#182), SPI
    documentation (#180), strip register prefixes (#190)

Common:

* Update to 2018 edition
* Updated cortex-m dependency to `>=0.5.8,<0.7.0` to allow use of new `0.6.0` (#176)
* Restructured derived peripherals to typically be from the first numbered
  peripheral, which causes some type names to change (#146)
* Stripped peripheral-name prefixes from many register names (#177, #187, #189,
    #190)
* Many peripherals updated to use clusters and arrays, leading to some
  breaking changes in svd2rust output (#116, #167)
* RCC updates for many devices (#142)
* Fix TIM2-5 `O24CE` to `OC4CE` in many devices (#157)
* Document USB registers in many devices (#162)
* Extend SPI coverage for F1, F2, and F3 (#150)
* UART fixes and documentation for F1, F2, and F7 (#153)
* `DBG` renamed to `DBGMCU` on many devices (#175)
* Add makefile target to format SVD files (`xmlformat`, #166)

Thanks to:

[@lochsh] [@jordens] [@aurelj] [@burrbull] [@jessebraham] [@therealprof]
[@mathk] [@hnez] [@solderjs] [@lichtfeind] [@arkorobotics] [@astro]
[@jkristell]

## [v0.6.0] 2019-01-14

Family-specific:

* F0: Extensively updated, RCC (#118, #130, #131), SYSCFG/COMP (#124), ADC (#129), SPI (#135)
* F1: Update RCC (#130)
* F2: RCC (#139)
* F4: USB OTG updated (#127), RCC (#130, #137)
* F7: RCC (#130, #137)
* L0: Fix wakeup pin bits in PWR_CSR (#120)
* G0: Introduced with basic support (#123)

Common:

* SPI: Added SSI, RXCRC, TXCRC (#138)
* We standardised on `Div8` style dividers, instead of `DIV8` or `DIV_8`.
* Travis builds now much faster (#134)
* Documentation links updated (#128)

Thanks to:

[@octronics] [@birkenfeld] [@dotcypress] [@aurelj] [@albru123] [@x37v]
[@HarkonenBade]

## [v0.5.0] 2018-12-16
* Now built on stable Rust
* Updated to svd2rust 0.14.0 (#108)
* Added patch support for rebasing peripherals (#98)
* Added patch support for arrays (#107)
* Added patch support for clusters (#112)

### Breaking Changes
* F0: Various fixes to RCC (#99, #114)
* F103: A few USB updates (#111)
* F103: Define a number of arrays and clusters (#112)
* F4: Various fixes to RCC (#95, #102)
* F4: Corrected UART Stop2 value (#103)
* L4: Various fixes to RCC (#101)
* L4: Fix USBFSEN (#92), other USB changes (#94)
* TIM: Various fixes (#96)

## [v0.4.0] 2018-11-13
* F7: Ethernet peripheral updates
* F0: ADC CFGR2 JITOFF_D* renamed CKMODE (#77)
* F4: Missing RCC enable/reset bits for various peripherals (#80)
* USART updated for most families (#75)
* F4: Ethernet peripheral updates (#81, #87)
* F4: RCC updates (#83)

## [v0.3.2] 2018-10-07
* F4: Update ethernet peripheral across entire family (#71, #73)

### Breaking Changes
* F4 ethernet MACMIIDR field TD is renamed MD to align with the reference
  manual

## [v0.3.1] fe63529 2018-10-07
* Fix typo in `tim16.yaml` that prevents builds on most devices

## [v0.3.0] 241ca45 2018-10-07
* H7x3: Add ETHERNET peripheral from scratch (#42)
* F0 and F1: GPIO updated (#49)
* F0: RCC updated (#58)
* L1: GPIO updated (#54)
* IWDG added for most devices (#45, #64)
* WWDG added for most devices (#48, #68)
* CRC added or updated for most devices (#46)
* Timers added or updated for most devices (#57)
* DMA added for most devices (#62)
* I2C added for most devices (#65)
* Supports Rust 1.30-beta for 2018 edition

### Breaking Changes
* Most I2C peripherals have their `SADDx`, `OA1x`, or `ADDx` registers merged
  into a single `SADD`, `OA1`, or `ADD` register. 7-bit addresses will need
  to be written shifted left by 1, i.e., in 8-bit mode.
  See https://github.com/adamgreig/stm32-rs/pull/65.

Thanks to [@ehntoo], [@octronics], [@burrbull], and [@MattCatz] for lots of
work in this release!

## [v0.2.3] c15e4a6 2018-09-07
* STM32F301: Fix incorrect aliasing of ADC.CSR and CCR
* STM32F4x9: Fix name of RM0386
* STM32F4: Improve timer coverage
* STM32F407: Include `TIM_OPM`
* Update to latest cortex-m-rt 0.6

## [v0.2.2] e648dae 2018-07-11
* Released crates now built with Form (#19, #29)
* Add a selection of documentation targets for docs.rs (#3)
* Many families: Add High/Low enum values for IDR/ODR on gpio_v2 (6c30cdc)
* Many families: Set DMA LIFCR and HIFCR to write-only (128b3d4)
* STM32F42{7,9}: Fix incorrect BWTR{3,4} (86dd104)
* STM32H7x3: Rename Flash->FLASH and fix PRAR_PRG2 (1e61674)
* STM32F7x{5,7,8,9}: Add PLLSAIRDY and PLLSAION (#35)

## [v0.2.1] 954966a 2018-07-02
* Add STM32L4x5 device (#28)
* Add PLLR field for STM32F7x7 (#30)
* Add missing interrupts for STM32F7 devices (#27)
* Add PWR peripheral to various devices
* Fix incorrect USART3EN (#34)
* Fix incorrect naming for STM32H7 (#26)

## [v0.2.0] 0c108b3 2018-06-12

* Changelog started
* Fix STM32H7x3 register naming (0c108b3)
* OS X compatibility
* Update cortex-m-rt to 0.5.1
* Update svd2rust to 0.13.1
* Fix nvicPrioBits being incorrect in many STM32s (de117ef)
* Add support for specifying interrupts and modifying CPU node

[Unreleased]: https://github.com/stm32-rs/stm32-rs/compare/v0.8.0...HEAD
[v0.8.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.7.0...v0.8.0
[v0.7.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.6.0...v0.7.0
[v0.6.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.5.0...v0.6.0
[v0.5.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.3.2...v0.4.0
[v0.3.2]: https://github.com/stm32-rs/stm32-rs/compare/v0.3.1...v0.3.2
[v0.3.1]: https://github.com/stm32-rs/stm32-rs/compare/v0.3.0...v0.3.1
[v0.3.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.2.3...v0.3.0
[v0.2.3]: https://github.com/stm32-rs/stm32-rs/compare/v0.2.2...v0.2.3
[v0.2.2]: https://github.com/stm32-rs/stm32-rs/compare/v0.2.1...v0.2.2
[v0.2.1]: https://github.com/stm32-rs/stm32-rs/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/stm32-rs/stm32-rs/compare/7b47b4...v0.2.0

[@ehntoo]: https://github.com/ehntoo
[@octronics]: https://github.com/octronics
[@burrbull]: https://github.com/burrbull
[@MattCatz]: https://github.com/MattCatz
[@birkenfeld]: https://github.com/birkenfeld
[@dotcypress]: https://github.com/dotcypress
[@aurelj]: https://github.com/aurelj
[@albru123]: https://github.com/albru123
[@x37v]: https://github.com/x37v
[@HarkonenBade]: https://github.com/HarkonenBade
[@lochsh]: https://github.com/lochsh
[@jordens]: https://github.com/jordens
[@jessebraham]: https://github.com/jessebraham
[@therealprof]: https://github.com/therealprof
[@mathk]: https://github.com/mathk
[@hnez]: https://github.com/hnez
[@lichtfeind]: https://github.com/lichtfeind
[@arkorobotics]: https://github.com/arkorobotics
[@astro]: https://github.com/astro
[@jkristell]: https://github.com/jkristell
[@solderjs]: https://github.com/solderjs
[@nickray]: https://github.com/nickray
[@richardeoin]: https://github.com/richardeoin
[@mabezdev]: https://github.com/mabezdev
