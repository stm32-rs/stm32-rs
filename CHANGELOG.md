# Changelog

## [Unreleased]

* Updated to `svd2rust` 0.36.1, `svdtools` 0.4.6, `form` 0.12.1, use tools binaries for CI (#1174)
* bump `defmt` dependency to 1.0
* Use `svd2rust.toml` config, use custom ident suffixes (#948)
* Replace `makehtml.py` with `svdtools html` (#881)
* Remove workaround for bug in duckscript's `mv` (#981)
* move `_array` and `_cluster` patches to `devices/collect` (#980)
* rename `devices/common_patches` to just `devices/patches` (#1066)
* move field related patches from `peripherals` to `devices/fields` (#1067)
* Normalized docs. Split (for `cargo make`) `form` task on `form` and `fmt` (#949)
* Show available device features if no one selected (#998)
* Add `download.sh` for fast source archives update (#1134)
* Add Open-CMSIS `svdconv` to for more checks (#908)
* Add `cargo make` `yamls` task for easy compare (#1050)
* Add `derivePathType` to CMSIS-SVD schema (#1025)
* Add possibility to publish crates with different versions (#1145)
* Enable atomic operations on register support, Rust edition 2021 (#846)
* files in devices/patches moved to subdirectories (#1066)
* remove executable file perm bit from yaml file (#854)
* TIM1/8 DMAR fix (#1172)
* HPDMA derive registers between CH and CH2D clusters (#1164)
* USART: refactor and add missing enums (#1156)
* Refactor timers, add enums (#1133)
* TIM: fix TS/SMS field names (#1186)
* Add placeholders for all peripherals (#1163)
* Fix DMA & collect (#1167)
* Format yamls: remove unneeded quotes (#1099)
* Apply existing RTC patches for new families, RTC alarm arrays (#1120)
* Manual enum names for EXRI & GPIO (#964)
* AES enums & patches (#1058)
* HPDMA: clusters (#1140)
* Derive GPIO registers (#1144)
* Fix yaml parsing errors (#1002)
* Collent in field arrays: ADC, GPIO, CAN, DSI, EXTI, SAI, DMA, TIM (#1097
* ADC: C0+G0+WL field arrays (#1051)
* Derive SYSCFG EXTI fields (#1108)
* modify `LP_Timer1` interrupt instead of adding new (#902)
* rename `KEY` field variants of `IWDG_KR` (#866)
* DMAMUX: merge registers in arrays (#873)
* move merge CAN FB fields in patch file (#904)
* G4, L5, U5 TIM common fixes (#912)
* Fix several array descriptions (#916)
* Fix ADC SQR ranges (#1102)
* Fix missing ADC.SMPR.SMPx_x (#1000)
* Fix EXTI_IMR_IM9 field, H7 DMAMUX cluster names (#891)
* Fix ADC SR OVR enums (#882)
* Fix ADC modifiedWriteValues (#1062)
* Add ADC enums for L4, L5, G0, H5, WB (#1062)
* Fix ETH_MACFFR bitOffsets (#903)
* Fix adding OTG_FS GCCFG NOVBUSSENS (#909)
* GFXMMU LUT cluster (#906)
* Fix writeConstraint bugs (#911)
* DMA ISR fixes for G0, G4 (#910)
* tools_install: support `$CARGO_HOME` environment variable (#953)
* Split `mmaps_pr` workflow on `mmaps_pr_generate` and `mmaps_pr_compare` (#949)
* TIM: rename & clean files (#800)
* Add GPIOx:HSLVR (#956)
* Fix incorrectly used `_read`, `_modify` (#968)
* `isDefault` for some RCC enums (#929)
* Doc `QUADSPI` peripheral (#875)
  `DR` register can be access by 1 byte, half word and full word. Use `.dr8()`, `.dr16()`, `.dr()` to access this register.
* 16-bit registers: IWDG, WWDG, U*ART (#1177)
* 16-bit SPI registers, add DR8 (#993) (fixed)
* 16-bit I2C registers (#995)
* U5/H5: collect GTZC registers in arrays (#1056)
* G0X1, G4, H5, H7R/S, L5, U5: Add UCPD peripheral (#1001)
* C0,G0,H5,U0: merge USB CHEP[0-7]R registers into array (#1036)
* C0,G0,H5: fix field names in cmmr1_output registers (#1038)
* LCD: fix and unify RAM registers (#1083)
* H5, U5: Add cluster definitions for GPDMA channels (#1121)
* F2, F4, F7: Add definitions for OPTCR, OPTCR1 and OPTCR2 registers of FLASH peripheral (#1157)
* F2, F4, F7: Fix several fields of FLASH peripheral and reorganise 'patches', 'fields' and 'collect' according to impacted registers (#1161)
* F1, F2, F4: Derive identical UART registers from USART1, add GPTR.PSC (#1179)
* CCMR3_Output fix
* CRC enums and fixes
* Add DAC enums
* DCMI enums
* DFSDM enums and fixes
* SDIO/SDMMC v1
* USB v2
* Use arrays for DAC channels
* Derive TIM registers
* Update README.md (#1152)
* Add SPI enums for G4, U5, H7+
* FMC/FSMC enums, arrays & derives
* CRS enums
* HRTIM:
  * H7 & G4 fixes and enums (#1021) (#1022)
  * Remove timer block suffixes from register/field names (#1023)
  * Derive identical registers (#1025)
  * Specify TIM events for each block (#1030)
* LPTIM v1/2

Family-specific:

* C0:
  * Initial support (#765)

* F1:
  * F103: USB RESP1 fix name (#927)
  * Remove CAN from F101/102 (#935)
  * Remove CAN2 from F103, rename CAN1 to CAN (#941)
  * Derive ADC registers/fields

* F3:
  * Update vendor SVD bundle to v1.3 (#1059)
  * F373 GPIOC LCKR, collect GPIO.BRR (#943)

* F4:
  * Update vendor SVD bundle to v2.0 (#1060)
  * doc on `SYSCFG` peripheral for STM32F4 (#852)
  * `PWR` peripherals for STM32F4 (#857)
  * doc on `RNG` peripheral for STM32F4 (#870)
  * Fix DAC for stm32f4 (#921)
  * F4: collect SDIO RESP (#932)

* F7:
  * Update vendor SVD bundle to v2.4 (#1085)

* G0:
  * Update vendor SVD bundle from v1.1 to v1.6 (#947) (#1012) (#1049)
  * remove Cortex-M0+ core peripherals (use `cortex-m` crate instead)
  * add enums for `RCC` & `SYSCFG`
  * `DMA?:IFCR` changed from read-only (wrong) to write-only
  * split `ADC:CHSELR1:CHSEL` into separate 1-bit fields
  * correct multiple fields in
    `EXTI`, `FLASH`, `PWR`, `RCC`, `TAMP`, and `SYSCFG`
  * Fix TIM1 CCMR?_Input fields (#912)
  * Fix typo in HSIDIV (Div3 -> Div4) (#1015)
  * G0B1: make TIM4 16-bit timer (#1035)
  * G0B1: force ARR field width to 16 bit when SVD describes ARR as 32-bit field for 16-bit timer (#1038)
  * G0: describe USB CHEP?R register (#1039)
  * Mark interrupt flags in USB ISTR as W0C (#1088)
  * Mark flags in USB CHEPR as W0C/W1T (#1088)
  * Add value enums for EXTICR[2-4] (#1088)
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
    * TIM3's CCRx is 16-bit (#1119)

* G4:
  * Update vendor SVD bundle to v2.2 (#1087)
  * Fix inconsistencies for HRTIM_TIMF - stm32g4x4 (#860)
  * Add dual bank flash related fields to g4 cat 3 devices (#880)
  * STM32G491: Add FDCAN2 peripheral (#915)
  * Fix typo in STM32G491 FDCAN2 patch (#917)
  * Fix swapped reset values for SPI4 CR1 and CR2 by deriving SPI4 from SPI1 (#957)
  * Merge USART BRR fields (#959)
  * Add USART v2C peripheral (#960)
  * Add DAC peripheral (#961)
  * COMP fix and collect array (#969)
  * Fix FDCAN interrupt numbers being swapped (#996)
  * G4A1: Add FDCAN2 and rename USB peripheral (#1003)
  * G4A1: Add BCDR and adjust to be closer to G491 (#1004)
  * G491 and G4A1: Add TIM20 (#1004)
  * G471: Add OPAMP6 (#1005)

* H5:
  * Update vendor SVD bundle to v1.7 (#1086) (#1124)
  * Add CRS, WWDG, IWDG, I2C, SBS, PWR, GPIO, EXTI, GPDMA, SPI, UART, RCC, TIM1-8 definitions (#956)
  * Add H523 (#1124)
  * STM32H503: Add missing RNG_NSCR register (#1148)
  * STM32H5xx: Add H533 (#1129)
  * Array gpio registers (#1053)
  * Add RCC defitions for H56x/H573 (#1033)

* H7:
  * Update vendor SVD bundle to v1.9 (#1092)
  * H72x/3x: add ADC3 fields
  * H735: add I2C5 (#864)
  * Update RNG for stm32h735 (#925)
  * Add bit TRBUFF of DMA_SxCR of H747 cm4 (#958)
  * Add stm32h7r/s devices (#972)
  * Fix GPIO register reset values (#973)
  * HRTIM H7 fix EECR3 (#1042)
  * HRTIM H7: delete DLL (#1044)
  * Add H723/25/30/33/42/50/55/A3/B0 (#1107)
  * RAMECC fixes & collect
  * RCC - Unify usbotg field naming and remove invalid fields (#1219)

* L0:
  * Update vendor SVD bundle to v1.4 (#1081)

* L1:
  * Update vendor SVD bundle to v1.4 (#1080)
  * L1 TIM9: add CCER (#905)
  * Fix ADC SMPR fieldFs in L1 (#1085)

* L4:
  * Update L4/L4+ vendor SVD bundles to v1.4 (#1084)
  * Add missing CAN registers to l4x3/x5 (#914)

* L5:
  * Fix DMA cluster (#922)

* MP1:
  * Fix DIGBYP bit access in RCC_BDCR (#1011)
  * Strip prefixes from peripherals (#1014)

* N6:
  * Initial support (#1211)

* U0:
  * Initial support (#1057)

* U5:
  * Update vendor SVD bundle to 1.3 (#844) (#890)
  * Add U535,45,95,A5,99,A9 (#844)
  * Strip prefixes from peripheral registers (#983)
  * Add ADC, DMA2D, EXTI, FMC, GPIO, I2C, OCTOSPI, PWR, RCC peripherals (#986)
  * MDF cluster (#1055)

* WB:
  * Update vendor SVD bundle to v1.2 (#1093)
  * Add `RCC`, `SYSCFG` enums (#777)

* WL:
  * Update vendor SVD bundle to v1.2 (#1093)

Contributors to this release:

[@adamgreig] [@astapleton] [@burrbull] [@David-OConnor] [@dotcypress]
[@datdenkikniet] [@Elemecca] [@eZioPan] [@FerdinandvHagen] [@FrigoreD] [@hydra]
[@ianic] [@iostat] [@jonathanherbst] [@jspngh] [@kevswims] [@liamkinne]
[@mattthebaker] [@newAM] [@noppej] [@rblaze] [@reitermarkus] [@richardeoin]
[@RootCubed] [@sorki] [@tdaede] [@Urhengulas] [@usbalbin] [@vinchatl]
[@YruamaLairba]

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
    * Copy L4x2-6 timers from L4x1
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

[@adamgreig]: https://github.com/adamgreig
[@astapleton]: https://github.com/astapleton
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
[@datdenkikniet]: https://github.com/datdenkikniet
[@DerFetzer]: https://github.com/DerFetzer
[@dgoodland]: https://github.com/dgoodland
[@diondokter]: https://github.com/diondokter
[@dirk-dms]: https://github.com/dirk-dms
[@disasm]: https://github.com/disasm
[@diseraluca]: https://github.com/diseraluca
[@dotcypress]: https://github.com/dotcypress
[@ehntoo]: https://github.com/ehntoo
[@Elemecca]: https://github.com/Elemecca
[@eupn]: https://github.com/eupn
[@eZioPan]: https://github.com/eZioPan
[@FerdinandvHagen]: https://github.com/FerdinandvHagen
[@FrigoreD]: https://github.com/FrigoreD
[@Geens]: https://github.com/Geens
[@Gekkio]: https://github.com/Gekkio
[@HarkonenBade]: https://github.com/HarkonenBade
[@helgrind]: https://github.com/helgrind
[@hnez]: https://github.com/hnez
[@hoachin]: https://github.com/hoachin
[@hydra]: https://github.com/hydra
[@ianic]: https://github.com/ianic
[@ijager]: https://github.com/ijager
[@iostat]: https://github.com/iostat
[@jamwaffles]: https://github.com/jamwaffles
[@JarLob]: https://github.com/JarLob
[@jessebraham]: https://github.com/jessebraham
[@jglauche]: https://github.com/jglauche
[@jhbruhn]: https://github.com/jhbruhn
[@jkristell]: https://github.com/jkristell
[@jonas-schievink]: https://github.com/jonas-schievink
[@jonathanherbst]: https://github.com/jonathanherbst
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
[@liamkinne]: https://github.com/liamkinne
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
[@mattthebaker]: https://github.com/mattthebaker
[@maximeborges]: https://github.com/maximeborges
[@newAM]: https://github.com/newAM
[@nickray]: https://github.com/nickray
[@noslaver]: https://github.com/noslaver
[@noppej]: https://github.com/noppej
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
[@rblaze]: https://github.com/rblaze
[@reitermarkus]: https://github.com/reitermarkus
[@rfuest]: https://github.com/rfuest
[@richard7770]: https://github.com/richard7770
[@richardeoin]: https://github.com/richardeoin
[@rmsc]: https://github.com/rmsc
[@RootCubed]: https://github.com/RootCubed
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
[@tdaede]: https://github.com/tdaede
[@therealprof]: https://github.com/therealprof
[@thinxer]: https://github.com/thinxer
[@tim-seoss]: https://github.com/tim-seoss
[@timblakely]: https://github.com/timblakely
[@timokroeger]: https://github.com/timokroeger
[@TomDeRybel]: https://github.com/TomDeRybel
[@torkeldanielsson]: https://github.com/torkeldanielsson
[@TwoHandz]: https://github.com/TwoHandz
[@Urhengulas]: https://github.com/Urhengulas
[@usbalbin]: https://github.com/usbalbin
[@vinchatl]: https://github.com/vinchatl
[@wallacejohn]: https://github.com/wallacejohn
[@Wassasin]: https://github.com/Wassasin
[@Windfisch]: https://github.com/Windfisch
[@X-yl]: https://github.com/X-yl
[@x37v]: https://github.com/x37v
[@YruamaLairba]: https://github.com/YruamaLairba
[@yusefkarim]: https://github.com/yusefkarim
