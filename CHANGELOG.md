# Changelog

## [Unreleased]

* Fix yaml parsing errors
* H7: add bit TRBUFF of DMA_SxCR of H747 cm4
* Fix inconsistencies for HRTIM_TIMF - stm32g4x4
* Collent in field arrays: GPIO, CAN, DSI, SAI, DMA, TIM
* L1 TIM9: add CCER
* F373 GPIOC LCKR, collect GPIO.BRR
* modify `LP_Timer1` interrupt instead of adding new
* Remove workaround for bug in duckscript's `mv`
* move `_array` and `_cluster` patches to `devices/collect`
* Replace `makehtml.py` with `svdtools html`
* Updated to `svd2rust` 0.33.4, `svdtools` 0.3.18, `form` 0.12.1, use tools binaries for CI
* Use `svd2rust.toml` config, use custom ident suffixes
* Normalized docs. Split (for `cargo make`) `form` task on `form` and `fmt`
* Show avaliable device features if no one selected (#998)
* Add Open-CMSIS `svdconv` to for more checks
* Enable atomic operations on register support, Rust edition 2021 (#846)
* files in devices/common_patches moved to subdirectories
* remove excutable file perm bit from yaml file (#854)
* rename `KEY` field variants of `IWDG_KR` ([#866])
* DMAMUX: merge registers in arrays
* move merge CAN FB fields in patch file
* Fix G0 TIM1 CCMR?_Input fields
* G4, L5, U5 TIM common fixes
* STM32U5xx: Update SVD to version 1.2 and add variants for xx=35,45,95,A5,99,A9 (#844)
* STM32U5xx: Update SVD to version 1.3 (#890)
* Fix several array descriptions
* Fix ADC SMPR fields in L1
* Fix missing ADC.SMPR.SMPx_x
* Fix EXTI_IMR_IM9 field, H7 DMAMUX cluster names
* Fix ADC SR OVR enums
* Fix ETH_MACFFR bitOffsets
* Fix adding OTG_FS GCCFG NOVBUSSENS
* GFXMMU LUT cluster
* Add missing CAN registers to l4x3/x5
* Remove CAN from F101/102
* Fix L5 DMA cluster
* Fix writeConstraint bugs
* STM32G491: Add FDCAN2 peripheral
* Fix typo in STM32G491 FDCAN2 patch
* DMA ISR fixes for G0, G4
* F103: USB RESP1 fix name
* F4: collect SDIO RESP
* Fix DAC for stm32f4 (#921)
* `PWR` peripherals for STM32F4 ([#857])
* tools_install: support `$CARGO_HOME` environment variable
* Update RNG for stm32h735
* H5: Add CRS, WWDG, IWDG, I2C, SBS, PWR, GPIO, EXTI, GPDMA, SPI, UART, RCC, TIM1-8 definitios
* TIM: rename & clean files
* Add GPIOx:HSLVR
* Add dual bank flash related fields to g4 cat 3 devices
* Merge USART BRR fields on G4
* Add G4 DAC peripheral
* Fix incorrectly used `_read`, `_modify`
* G4:COMP fix and collect array
* Add USART v2C peripheral on G4
* doc on `RNG` peripheral for STM32F4 ([#870])
* `isDefault` for some RCC enums
* H7: fix GPIO register reset values (#973)
* H735: add I2C5
* Doc `QUADSPI` peripheral ([#875])
    * `DR` register can be access by 1 byte, half word and full word. Use `.dr8()`, `.dr16()`, `.dr()` to access this register.
* 16-bit SPI registers, add DR8 (#993) (fixed)
* 16-bit I2C registers (#995)
* U5: Strip prefixes from peripheral registers
* U5: Add ADC, DMA2D, EXTI, FMC, GPIO, I2C, OCTOSPI, PWR, RCC peripherals
* H7: add stm32h7r/s devices (#972)
* WB: add `RCC`, `SYSCFG` enums
* G4: fix FDCAN interrupt numbers being swapped
* G0X1, G4, H5, H7R/S, L5, U5: Add UCPD peripheral
* G4A1: Add FDCAN2 and rename USB peripheral
* G4A1: Add BCDR and adjust to be closer to G491
* G491 and G4A1: Add TIM20
* G471: Add OPAMP6

Family-specific:

* GO:
  * Update vendor SVD bundle from v1.1 to v1.5 (#947)
    * remove Cortex-M0+ core peripherals (use `cortex-m` crate instead)
    * add enums for `RCC` & `SYSCFG`
    * `DMA?:IFCR` changed from read-only (wrong) to write-only
    * split `ADC:CHSELR1:CHSEL` into separate 1-bit fields
    * correct multiple fields in
      `EXTI`, `FLASH`, `PWR`, `RCC`, `TAMP`, and `SYSCFG`
    * G030/G031/G041:
      * rename `DMA` to `DMA1`
      * remove `DMA_Channel4_5_6_7` interrupt from `DMAMUX`
        (replaced by `DMA1_Channel_4_5_DMAMUX` in `DMA1`)
      * move `PVD` interrupt from `EXTI` to `PWR`
      * move `ITLINE*` registers from `SYSCFG_ITLINE` to `SYSCFG`
    * G050/G051/G061:
      * add missing peripherals `AES` (G061), `COMP`, `DBG`, `DMA1`, `EXTI`,
        `FLASH`, `GPIO?`, `LPUART1` (G0x1), `PWR`, `RCC`, `RNG` (G061),
        `RTC`, `SPI?`, `SYSCFG`, and `TAMP`
      * `USART?:CR1`: change `RXFNEIE` to `RXNEIE` and `TXFNEIE` to `TXEIE`
      * remove `DMA1_Channel4_5_6_7_DMAMUX_DMA2_Channel1_2_3_4_5` interrupt
        from `DMAMUX` (replaced by `DMA1_Channel_4_5_6_7_DMAMUX` in `DMA1`)
      * remove register prefix from `LPTIM[12]` (G0x1)
    * G070/G071/G081:
      * remove non-existent registers `HWCFG*`, `VERR`, `IPIDR`, and `SIDR`
        from `ADC`, `RTC`, and `TAMP`
      * rename `DMA` to `DMA1`
      * remove `DMA_Channel4_5_6_7` interrupt from `DMAMUX`
        (replaced by `DMA1_Channel_4_5_6_7_DMAMUX` in `DMA1`)
      * split `SYSCFG_VREFBUF` peripheral into `SYSCFG` and `VREFBUF` (G0x1)
    * G0B0:
      * add missing peripherals `ADC`, `EXTI`, `FLASH`, `I2C3`,
        `PWR`, `RCC`, `RTC`, `SPI?`, `SYSCFG`, `TAMP`, `TIM4`, `USB`
      * `USART?`: many changes to `CR1` and `ISR`
      * remove `DMA_Channel4_5_6_7` interrupt from `DMAMUX` (replaced by
        `DMA1_Channel_4_5_6_7_DMAMUX_DMA2_Channel1_2_3_4_5` in `DMA1`)
      * rename `I2C2` interrupt to `I2C2_I2C3`
      * rename `TIM3` interrupt to `TIM3_TIM4`
    * G0B1/G0C1:
      * add missing peripheral `SYSCFG`
      * fix `SPI` register sizes
      * remove `TIM6_DAC` interrupt
      * `USART?`: many changes to `CR1` and `ISR`
      * add `DMA?` interrupts

[#854]: https://github.com/stm32-rs/stm32-rs/pull/854
[#857]: https://github.com/stm32-rs/stm32-rs/pull/857
[#866]: https://github.com/stm32-rs/stm32-rs/pull/866
[#870]: https://github.com/stm32-rs/stm32-rs/pull/870
[#875]: https://github.com/stm32-rs/stm32-rs/pull/875

## [v0.15.1] 2022-07-04

* Updated to svd2rust 0.24.1 to fix critical codegen issue (#751)
* Fix FSDEF field being marked read-only in SAI (#752)

## [v0.15.0] 2022-07-04

This release has been yanked from crates.io as it was generated using svd2rust
0.24.0 which suffered from a codegen bug (see #748).

Common changes:

* Strip prefixes from many peripheral registers (#661)
* Add `SVDTOOLS` env value for specifying patching tool (#673)
* Fix HTML generation on macOS (#679)
* Replace Python svd tools with Rust alternatives (#701)
* Added missing TIMx:CR1:OPM, removed unused CNT_H, ARR_H, CCR_H (#684)
* Use PascalCase for generated values of enums (#727)
* Updated to svd2rust 0.24.0 (#733)
* Document RTC ALARM and BKPR (#724)
* Extensive internal refactor of GPIO patches (#717)
* Change groupName of ADC_Common to ADC_Common (#719)
* Fix field access on many SAI fields (#691)

Family-specific:

* G0:
    * G0B1/G0C1: Update SVDs (#666)
    * G0B1/G0C1: Fix previous incorrect deletion of DMA1/2 (#675)
    * Clear all vendor provided enumeratedValues (#686)
    * Update SVDs, document DMA, various other patches (#687)
    * Make FLASH_WRP??R and FLASH_SECR writeable (#690)
    * G070: Rename SYSCFG_VREFBUF to SYSCFG, remove VREFBUF registers (#716)
    * Fix DMA and TIM15 register field names (#695)

* G4:
    * Fix ADC ADSTP, ADSTART, ADDIS, ADEN bit enumerations (#699)
    * Remove RNGSMEN -> RNGEN renaming to have AHB2SMENR.RNGSMEN (#729)

* H7:
    * h747: add midding DSI interrupt (#646)
    * h735, h7b3: remove unavailable DSI peripheral (#648)
    * Make ETH_MAC MMC mask register writable (#658)
    * RM0455: Fix incorrect rename of OCTOSPI peripheral (#653)
    * Arrayify HASH registers (#663)
    * Add bit ranges to HDMI CRC registers (#671)
    * H743/H753: Fix Overdrive and BDMADR fields (#649)
    * h7b3: clear all enumeratedValues (#686)
    * Change DMA CR to only cover SxCR, not LIFCR and HIFCR (#702)
    * H735: Add TIM23 and TIM24 (#712)
    * Fix ADC ADSTP, ADSTART, ADDIS, ADEN bit enumerations (#699)
    * Arrayify HSEM registers (#735, #737)
    * h747: add flash registers mirrored in bank2 (#704)
    * H735: Add CORDIC and FMAC peripherals (#677)
    * H735: Add missing TIM1, DCMI, OTG USB, RNG, LTDC, RAMECC interrupts (#677)
    * Rename DBGSTBD1, DBGSTPD1, DBGSLPD1 fields to match RM (#677)
    * RM0468: Add UART9/USART10, RM0455: fix USART base addresses (#652)

* F0:
    * F0x1/2/8: Add bit ranges to HDMI CRC registers (#671)
    * Add missing CRC POL register (#710)

* F2:
    * Fix incorrect bit position for Ethernet MMCTIMR TGFM (#689)
    * Add ADC EXTSEL enumerations (#707)
    * Apply existing OTG_FSv1 fixes (#706)

* F3:
    * Add missing 'P' to JADST (#696)
    * Fix ADC ADSTP, ADSTART, ADDIS, ADEN bit enumerations (#699)
    * Fix various fields access (#734)
    * F302: Rename `DAC` to `DAC1` (#742)

* F4:
    * F469: Fix `DSIHSOT_CCR` register name (#664)
    * Fix incorrect bit position for Ethernet MMCTIMR TGFM (#689)
    * F411: Fix OTG_FS registers (#697)
    * Add ADC EXTSEL enumerations (#707)
    * Add GTPR register to UART (#713)
    * Document TIM2 ITR1_RMP enums (#678)
    * F410/411/412: add BDCR LSEMOD field (#708)

* F7:
    * Add SDMMC2EN and SDMMC2RST to F765, F7x7, F7x9 (#662)
    * Fix incorrect bit position for Ethernet MMCTIMR TGFM (#689)
    * Add bit ranges to HDMI CRC registers (#671)
    * Add ADC EXTSEL enumerations (#707)
    * Fix ADC DR RDATA name and description (#723)
    * Document safe ranges for CNT/ARR/CCR (#700)
    * Arrayify JPEG memory registers (#725)

* L0:
    * Re-add TIM21/TIM22 (#659)
    * Fix various fields access (#734)

* L4:
    * Add documentation for FIREWALL (#660)
    * Arrayify HASH registers (#663)
    * L4R9: Fix `DSIHSOT` interrupt name (#664)
    * L4R9: Add TIM3 and TIM4 (#669)
    * L4x5/6/R9: Rename DBGMCU APB_FZR to remove underscores (#681)
    * Add GPIOx ASCR and BRR registers (#680)
    * Added missing channel 2 on TIM15 (#705)
    * Fix ADC RDATA field name and description. (#723)
    * Add more enums for clock selection registers (#720)
    * Rename `Polynomialcoefficients` field to `POL` (#710)
    * Remove COMP1/COMP2 prefix from field names, document fields (#682)
    * Add L4R5 device (#740)

* L5:
    * Fix DMA CCR fields, arrayify GTZC VCTR (#715)

* WB:
    * Arrayify HSEM registers (#735, #737)

* WL:
    * Put all timers into common TIM group (#657)
    * Fix various fields access (#734)
    * Arrayify HSEM registers (#735, #737)

Contributors to this release:

[@LeonSkoog] [@kenbell] [@ryan-summers] [@burrbull] [@richardeoin]
[@systec-ms] [@DerFetzer] [@newAM] [@jspngh] [@jamwaffles] [@sephamorr]
[@MathiasKoch] [@omion] [@davidlattimore] [@Sh3Rm4n] [@Windfisch] [@sorki]
[@taylorh140] [@reitermarkus] [@larchuto] [@jonas-schievink] [@tim-seoss]
[@Wassasin] [@Gekkio] [@korken89] [@maximeborges] [@sphw] [@dgoodland]
[@X-yl] [@disasm] [@Pagten] [@oldsheep68] [@TomDeRybel] [@mattcarp12]

## [v0.14.0] 2021-10-02

Family-specific:

* F0:
    * Fix duplicated aliased registers WAIT/AUTDLY and DMAEN/DMA1EN (#538)
* F3:
    * Mark HRTIM ISR FLT fields read-write (#592)
    * Fix reset value for FLASH OBR (#600)
* F4:
    * Add FLASH and PLLR description for F446 (#533)
    * Add FLTR register to all I2C peripherals (#534)
    * Rename DSIHOST to DSI for F469 (#585)
    * Fix UART RCC enable/reset bits (#589)
    * Remove non-existant TIM8 from F401 (#633)
* F7:
    * Strip DSI prefix from DSI registers (#585)
    * Fix reset value for RCC DCKCFGR (#600)
    * Fix all timer registers (#606)
    * Fix all SYSCFG registers (#612)
    * Fix all RCC registers (#613)
    * Fix all SDMMC registers (#620)
    * Fix CRC INIT and POL register offsets (#632)
* L0:
    * Add L0x0 family (#505)
    * Fix TIM CNT, ARR, CCR register sizes (#581)
    * Fix RCC_CSR RMVF bit offset in L0x2 and L0x3 (#566)
* L4:
    * Fix ADC SQR1.L name and description (#519)
    * Add missing APB1RSTR1.USBFSRST field for L4x3 (#526)
    * Fix AHB1 CRC bits for L4x3 (#517)
    * Add STM32L4R9 (#532)
    * Add SPI register descriptions (#535)
    * Strip DSI prefix from DSI registers (#585)
    * Fix RTC registers in L41x and L42x (#580)
    * Add USB_BCDR register, fix USB base address, and add USB interrupt (#580)
    * Add CRSEN to APB1ENR1 (#580)
    * Fix bit offset for CRC and USART bits in RCC (#571)
    * Fix LCD RAM_COM register size and arrayify (#552)
* L5:
    * Fix TIM15 CCR2 address offset (#518)
* H7:
    * Add WWDG field descriptions (#502)
    * Add DAC2AMEN to H7B3 (#500)
    * Add LTDC field descriptions (#512)
    * Fix FDCAN_TEST register to be writable (#574)
    * Update to latest ST SVDs and add H72x/H73x devices (#554)
    * Fix invalid patches to RCC registers (#615)
    * Fix and cluster DFSDM registers (#637)
    * Add SAI CR1 NOMCK alias bit to H743/753 and remove MCKEN (#640)
* G0:
    * Update to new ST SVD release (#514)
* G4:
    * Add I2C register definitions (#510)
    * Add USB BCDR register (#506)
    * Add GPIO register definitions (#531)
    * Add more descriptions for RCC (#528)
* WB:
    * Enable in nightly releases (#509)
    * Fix ADC SQR1.L name and description (#519)
    * Add missing EXTI fields (#580)
    * Fix TIM16 CR1 (#580)
    * Rename ADC to ADC1, add new ADC_Common peripheral (#623)
    * Fix SYSCFG register offsets (#624)
    * Fixes for ADC, TIM16, and TIM17 (#625)
    * Rename EXTI10_15 and EXTI5_9 interrupts to EXTI15_10 and EXTI9_5 (#634)
    * Fix TIM2.CNT bit width (#635)
* WL:
    * Update to new ST SVD release (#507)
    * Extensive patches and descriptions for WLE5, covering many peripherals (#559)
    * Unify EXTI.IMRx for WLE5 to match dual-core parts (#590)
    * Fix EXTI14 enumerated values (#599)
    * Add register descriptions for dual-core variants (#628)
* MP:
    * Strip DSI prefix from DSI registers (#585)
    * Add initial support for STM32MP153 device (#614)

Common:

* Many devices using USART "v2" had write constraints fixed to allow 9-bit
  words, affecting F0, F3, F7, H7, L0, L4, and WL families. (#558)
* The `rt` feature is now enabled by default; use `default-features=false` to
  disable (#582).
* Updated to svd2rust 0.19, with changes to the generated crate API.
  This update required a number of fixes to bugs in the SVD files,
  especially including fixes to timers across all families (#540, #546, #596).
* Fix a bug causing aliased registers to be suppressed in the HTML output
  (#591)
* Added a register map to HTML output (#598).
* Allow generating HTML output for selected families only (#607).
* Cortex-m-rt version 0.7 is now supported (#595, #603).

Contributors to this release:

[@diondokter] [@mattico] [@noslaver] [@jglauche] [@ofauchon] [@richardeoin]
[@Geens] [@wallacejohn] [@kevswims] [@qwandor] [@cyrusmetcalf] [@ByteNaked]
[@cyberillithid] [@kenbell] [@tachiniererin] [@yusefkarim] [@lynaghk]
[@sirhcel] [@timblakely] [@lulf] [@ijager] [@jorgeig-space] [@burrbull]
[@timokroeger] [@newAM] [@maximeborges] [@David-OConnor] [@rmsc] [@jhbruhn]
[@karlp] [@AndreasKarg]

## [v0.13.1] 2021-06-02

This version has only been released as a patch release for the
stm32f3 family.

* F3:
    * Backport #558 to allow use in Discovery book

## [v0.13.0] 2021-02-06

Family-specific:

* F3:
    * Fix GPIO OSPEEDR variants (#466)
    * Remove F3x8 device, which is now supported by F303 device (#495)
    * Rename DAC to DAC1 and add DAC2 to F303 (#497)
    * Correct EXTI IMR2/EMR2/RTSR2/FTSR2/SWIER2 addresses (#496)
* F4:
    * Fix ADC SMPR registers (#460)
    * Fix and document LTDC peripheral (#448)
    * Add OTG_FS interrupt to F413 (#470)
    * Add DSIHOST interrupt to F469 (#498)
* F7:
    * Add missing CRC fields (#447)
    * Fix and document LTDC peripheral (#448)
    * Add STM32F750 device (#464)
* L4:
    * Add ADC common register (#463)
    * Rename ADC to ADC1, add ADC2 (#465)
    * Add missing SMPR fields to ADC (#484)
    * Fix ADC CCR CH17SEL/CH18SEL field names (#491)
* L5:
    * Fix L552 TIMx interrupts (#468)
    * Add missing CPU blocks to SVD file (#476)
    * Add GPIO enum variants (#479)
    * Add RCC enum variants (#472)
    * Add basic FDCAN support (#478)
* G0:
    * Update which devices are built on docs.rs (#442)
* G4:
    * Fix incorrect IWDG/WWDG addresses (#475)
    * Fix SP3EN field name to SPI3EN (#481)
    * Add basic FDCAN support (#478)
    * Add CORDIC descriptions (#485)
    * Update to newest SVD files, adding G491 and G4A1 devices (#492)
    * Document OPAMP registers (#486)
* H7:
    * Array RTC_BCKP registers (#445)
    * Document RTC registers (#446)
    * Enable broken DMAMUX patch for H7B3 (#453)
    * Add/fix interrupts for H7B3 (#449)
    * Add cluster for MDMA registers (#454)
    * Fix CRC INIT and POL register addresses (#458)
    * Add basic FDCAN support (#478)
    * H7B3: Add DAC2 fields, remove LPTIM4/5 fields from RCC (#499)
* WL:
    * Family added with STM32WLE5 chpi (#444)
* WB:
    * Family added with STM32WB55 chip (#467)
* MP1:
    * Add missing CPU blocks to SVD file (#476)
    * Add basic FDCAN support (#478)

Common:

* Fixed a security issue in CI scripts (b7f023c),
  GHSL-2020-278 (thanks to [@JarLob]).
* CRC IDR set as 8 or 32 bit as appropriate across many families (#461)
* Fix description for RCC SWS field in many devices (#482)
* Fix misspelled MCJDIV to MCKDIV field in SAI CR1 register across many
  devices in f4, f7, f4, l4, l5, and wb55 families (#490)
* Fix misspelled WCKSEL to WUCKSEL field in RTC CR register across many
  devices in f2, g4, l1, l4, and wb55 (#494)

Thanks to:

[@ijager] [@mattico] [@chengsun] [@richardeoin] [@maximeborges]
[@AlyoshaVasilieva] [@YruamaLairba] [@korken89] [@Piroro-hs] [@eupn]
[@kenbell] [@matoushybl] [@diseraluca] [@TwoHandz] [@pawelchcki]
[@wallacejohn]

## [v0.12.1] 2020-09-22

* Fixes a bug introduced by a new version of svdtools which resulted in
  missing interrupts for devices which used `_copy` in their patches (see #440)

## [v0.12.0] 2020-09-20

Family-specific:

* F0:
    * Fix CRC INIT address (#407)
* F1:
    * F107 Ethernet and USB OTG support (#380)
* F3:
    * Document RTC (#373)
    * Document SYSCFG (#375)
    * Fix typos in OPAMP (#391)
    * Fix GPIO reset values (#406)
    * Add missing GPIO bits to f3x8 (#411)
* F4:
    * Document flash on F401 (#374)
    * F412 FSMC cleanup (#379)
    * Update SDIO fields (#383)
    * Rename I2C4 to FMPI2C1 and document it (#390)
    * Fix F446 SDIO (#393)
    * Add missing interrupts to F412 (#429)
* F7:
    * Fix typo in I2C enumeration variant (#433)
* L0:
    * Fix CCM missing bits on TIM21 (#415)
* L4:
    * Rename DMA interrupts for L4x3, 4x5, 552, 562 to match RM (#435)
* L5:
    * Add basic STM32L5 support (#371)
* G0:
    * Split G07x into G070 and G071 (#395)
    * Fixes for G070, G071, G081 (#398)
    * Group DMA registers (#408)
* H7:
    * Add basic H7B3 support (#378)
    * Remove DBGSTDBY_D3 and DBGSTOP_D3 bits (#385)
    * Document CCR and CCMR for TIM12-17 (#392)
    * Rename USBxOTGHSEN to USBxOTGEN, USBxOTGULPIHSEN to USBxULPIEN (#401)
    * Add Basic DMA (#403)
    * Fix UART7LPEN fixes (#404)
    * Add missing TRBUFF bit (#414)
    * RCC CCIP patches, SDMMC prefix for b3 (#416)
* MP1:
    * Update tooling to support family names with more than one letter (#423)
    * Add preliminary support for MP1 family (#425)

Common:

* Document CRC for F3, F7, H7, L0, L4 (#376)
* Swap to GHA for CI (#377)
* Fix Makefile for MacOS (#396)
* writeConstraints removed for DMA address registers (#400)
* Add virtual DR8 and DR16 registers to advanced CRC peripheral (#412)
* Spelling mistake in description for timer registers (#422)
* Support running makecrates.py for specific families (#424, #428)
* Fix duplicated enumeratedValues on some fields (#426)
* Add default-target per-family to docs.rs build (#427)
* Fix incorrect writeConstraint maximum of 65536 to 65535 on some fields (#434)
* Various fixes to ensure generated SVD files are compliant with schema

Thanks to:

[@Sh3Rm4n] [@yusefkarim] [@richardeoin] [@samcrow] [@torkeldanielsson]
[@jkristell] [@aurelj] [@helgrind] [@cyberillithid] [@ijager] [@ra-kete]
[@Pagten] [@mattico] [@almusil] [@diondokter] [@maximeborges] [@Rahix]
[@Piroro-hs]

## [v0.11.0] 2020-04-25

Family-specific:

* F0:
    * Fix width of TIM1 and TIM14-17 registers (now 16 bit) (#363)
* F3:
    * Flash documentation (#368)
    * Fix duplicate FPU interrupts (#357)
* F4:
    * Add missing interrupts (#360, #362, #341)
    * Fix duplicate FPU interrupts (#357)
    * Fix FSMC peripheral base address (#354)
    * RNG documentation (#348)
    * Links fixed in device table (#343)
    * Fix DMA CR.CHSEL width (#339)
    * Fix build error on Windows (#369)
* F7:
    * Fix DMA CR.CHSEL width (#339)
* H7:
    * HDMICRC renamed to CRC (#367)
    * Add SYSCFG_PWRCR register (#366)
    * Apply flash bank grouping to all parts (#364)
    * AXI documentation (#359)
    * RAMECC registers and documentation (#353)
    * SAI documentation and fixes (#347)
* L4:
    * Fix duplicate FPU interrupts (#357)
    * RCC field name fixes (#350)
* G4:
    * ADC documentation (#338)

Common:

* Fixed typo in I2C `OA1EN` `Disabled` variant name for many devices (#365)
* Hopefully fixed docs.rs building (#355)
* Generated crate directories no longer stored in git (#346)

Thanks to:

[@Sh3Rm4n] [@richardeoin] [@hoachin] [@BryanKadzban] [@richardeoin]
[@aurabindo] [@MarcoIeni] [@therealprof] [@ryan-summers] [@dirk-dms]
[@aurelj] [@tachiniererin] [@torkeldanielsson]

## [v0.10.0] 2020-02-13

Family-specific:

* F0:
    * ADC documentation (#307)
    * EXTI documentation (#314)
    * Fix number of interrupt priority bits (#325)
* F1:
    * EXTI documentation (#314)
* F2:
    * ADC documentation (#306)
    * DMA documentation (#322)
    * EXTI documentation (#314)
* F3:
    * ADC documentation (#305)
    * GPIO documentation for F373 and F3x8 (#321)
    * EXTI documentation (#314)
    * Add COMP interrupts (#302)
* F4:
    * ADC documentation (#313)
    * Add missing reset and enable registers in AHB3 (#311)
    * EXTI documentation (#314)
    * DMA2D documentation (#333)
* F7:
    * ADC documentation (#310)
    * DMA documentation (#322, #329)
    * Add STM32F730 (#316)
    * EXTI documentation (#314)
    * DMA2D documentation (#333)
* H7:
    * ADC documentation (#312)
    * Fix EXTI access in single-core parts (#318)
    * DMA documentation (#322)
    * EXTI documentation (#314)
    * Further dual core support (#319)
    * DMA2D documentation (#333)
    * Split SOF field in DMAMUX.CSR (#336)
* L0:
    * Fix FLASH_SR.EOP access (#309)
    * EXTI documentation (#314)
* L4:
    * Fix USART3RST in RCC (#243)
    * Fix APB1ENR1 SPI2EN name (#315)
    * EXTI documentation (#314)
* G0:
    * Fix number of interrupt priority bits (#304)
    * EXTI documentation (#314)
* G4:
    * EXTI documentation (#314)
    * Fix comparator register offsets (#335)

Common:

* Remove `scripts/svdpatch.py` and use `svdtools` (#331)
* Added new nightlies repository which can be directly used in Cargo: [nightlies]

Thanks to:

[@aurelj] [@dotcypress] [@hannobraun] [@samcrow] [@korken89] [@richardeoin]
[@rfuest] [@Sh3Rm4n] [@nickray] [@thinxer] [@lynaghk]

[nightlies]: https://github.com/stm32-rs/stm32-rs-nightlies

## [v0.9.0] 2019-11-10

Family-specific:

* F1:
    * F100 ADC (#270)
* F3:
    * ADC, COMP, DAC, HRTIM, OPAMP (#287)
    * HRTIM interrupt numbers (#289)
    * Update README concerning parts in each module (#295)
* F4:
    * F401 and F411 USB OTG FS patch (#272)
* F7:
    * Update SVD files to latest from vendor (#299)
* L0:
    * L0xx: NVIC priority bits (#275)
    * L0xx: fixes (#291, #292, #293)
    * L0x1: RCC APB1ENR TIM3 fix (#297)
    * L0xx: SYSCFG CFGR3 fixes (#300)
* H7:
    * Add dual core parts (#276, #285)
    * Correct PLL2DIVR names (#281)
    * Split ethernet peripheral in dual core parts (#288)
* G0:
    * Update G0 SVD files (#286)
* G4:
    * RCC fixes (#294)

Common:

* OTG HS patches (#272, #274)
* Updated to svd2rust 0.16.1 (#271, #283)
* Explicitly open YAML files in UTF-8 (#277)
* Makefile improvements (#278, #279, #280)
* svdpatch supports copying peripherals from another SVD (#298)

Thanks to:

[@burrbull] [@disasm] [@albru123] [@kitzin] [@richardeoin] [@dotcypress]
[@richard7770] [@jonas-schievink] [@ajfrantz] [@aurelj] [@osannolik] [@rfuest]

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

[Unreleased]: https://github.com/stm32-rs/stm32-rs/compare/v0.15.0...HEAD
[v0.15.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.14.0...v0.15.0
[v0.14.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.13.0...v0.14.0
[v0.13.1]: https://github.com/stm32-rs/stm32-rs/compare/v0.13.0...v0.13.1
[v0.13.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.12.1...v0.13.0
[v0.12.1]: https://github.com/stm32-rs/stm32-rs/compare/v0.12.0...v0.12.1
[v0.12.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.11.0...v0.12.0
[v0.11.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.10.0...v0.11.0
[v0.10.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.9.0...v0.10.0
[v0.9.0]: https://github.com/stm32-rs/stm32-rs/compare/v0.8.0...v0.9.0
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

[@ajfrantz]: https://github.com/ajfrantz
[@albru123]: https://github.com/albru123
[@almusil]: https://github.com/almusil
[@AlyoshaVasilieva]: https://github.com/AlyoshaVasilieva
[@AndreasKarg]: https://github.com/AndreasKarg
[@arkorobotics]: https://github.com/arkorobotics
[@astro]: https://github.com/astro
[@aurabindo]: https://github.com/aurabindo
[@aurelj]: https://github.com/aurelj
[@birkenfeld]: https://github.com/birkenfeld
[@BryanKadzban]: https://github.com/BryanKadzban
[@burrbull]: https://github.com/burrbull
[@ByteNaked]: https://github.com/ByteNaked
[@chengsun]: https://github.com/chengsun
[@cyberillithid]: https://github.com/cyberillithid
[@cyrusmetcalf]: https://github.com/cyrusmetcalf
[@David-OConnor]: https://github.com/David-OConnor
[@davidlattimore]: https://github.com/davidlattimore
[@DerFetzer]: https://github.com/DerFetzer
[@dgoodland]: https://github.com/dgoodland
[@diondokter]: https://github.com/diondokter
[@dirk-dms]: https://github.com/dirk-dms
[@disasm]: https://github.com/disasm
[@diseraluca]: https://github.com/diseraluca
[@dotcypress]: https://github.com/dotcypress
[@ehntoo]: https://github.com/ehntoo
[@eupn]: https://github.com/eupn
[@Geens]: https://github.com/Geens
[@Gekkio]: https://github.com/Gekkio
[@HarkonenBade]: https://github.com/HarkonenBade
[@helgrind]: https://github.com/helgrind
[@hnez]: https://github.com/hnez
[@hoachin]: https://github.com/hoachin
[@ijager]: https://github.com/ijager
[@jamwaffles]: https://github.com/jamwaffles
[@JarLob]: https://github.com/JarLob
[@jessebraham]: https://github.com/jessebraham
[@jglauche]: https://github.com/jglauche
[@jhbruhn]: https://github.com/jhbruhn
[@jkristell]: https://github.com/jkristell
[@jonas-schievink]: https://github.com/jonas-schievink
[@jordens]: https://github.com/jordens
[@jorgeig-space]: https://github.com/jorgeig-space
[@jspngh]: https://github.com/jspngh
[@karlp]: https://github.com/karlp
[@kenbell]: https://github.com/kenbell
[@kevswims]: https://github.com/kevswims
[@kitzin]: https://github.com/kitzin
[@korken89]: https://github.com/korken89
[@larchuto]: https://github.com/larchuto
[@LeonSkoog]: https://github.com/LeonSkoog
[@lichtfeind]: https://github.com/lichtfeind
[@lochsh]: https://github.com/lochsh
[@lulf]: https://github.com/lulf
[@lynaghk]: https://github.com/lynaghk
[@mabezdev]: https://github.com/mabezdev
[@MarcoIeni]: https://github.com/MarcoIeni
[@MathiasKoch]: https://github.com/MathiasKoch
[@mathk]: https://github.com/mathk
[@matoushybl]: https://github.com/matoushybl]
[@mattcarp12]: https://github.com/mattcarp12
[@MattCatz]: https://github.com/MattCatz
[@mattico]: https://github.com/mattico
[@maximeborges]: https://github.com/maximeborges
[@newAM]: https://github.com/newAM
[@nickray]: https://github.com/nickray
[@noslaver]: https://github.com/noslaver
[@octronics]: https://github.com/octronics
[@ofauchon]: https://github.com/ofauchon
[@oldsheep68]: https://github.com/oldsheep68
[@omion]: https://github.com/omion
[@osannolik]: https://github.com/osannolik
[@Pagten]: https://github.com/Pagten
[@pawelchcki]: https://github.com/pawelchcki
[@Piroro-hs]: https://github.com/Piroro-hs
[@qwandor]: https://github.com/qwandor
[@ra-kete]: https://github.com/ra-kete
[@Rahix]: https://github.com/Rahix
[@reitermarkus]: https://github.com/reitermarkus
[@rfuest]: https://github.com/rfuest
[@richard7770]: https://github.com/richard7770
[@richardeoin]: https://github.com/richardeoin
[@rmsc]: https://github.com/rmsc
[@ryan-summers]: https://github.com/ryan-summers
[@samcrow]: https://github.com/samcrow
[@sephamorr]: https://github.com/sephamorr
[@Sh3Rm4n]: https://github.com/Sh3Rm4n
[@sirhcel]: https://github.com/sirhcel
[@solderjs]: https://github.com/solderjs
[@sorki]: https://github.com/sorki
[@sphw]: https://github.com/sphw
[@systec-ms]: https://github.com/systec-ms
[@tachiniererin]: https://github.com/tachiniererin
[@taylorh140]: https://github.com/taylorh140
[@therealprof]: https://github.com/therealprof
[@thinxer]: https://github.com/thinxer
[@tim-seoss]: https://github.com/tim-seoss
[@timblakely]: https://github.com/timblakely
[@timokroeger]: https://github.com/timokroeger
[@TomDeRybel]: https://github.com/TomDeRybel
[@torkeldanielsson]: https://github.com/torkeldanielsson
[@TwoHandz]: https://github.com/TwoHandz
[@wallacejohn]: https://github.com/wallacejohn
[@Wassasin]: https://github.com/Wassasin
[@Windfisch]: https://github.com/Windfisch
[@X-yl]: https://github.com/X-yl
[@x37v]: https://github.com/x37v
[@YruamaLairba]: https://github.com/YruamaLairba
[@yusefkarim]: https://github.com/yusefkarim
