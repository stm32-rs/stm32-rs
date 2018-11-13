# Changelog

## v 0.4.0 2018-11-13
* F7: Ethernet peripheral updates
* F0: ADC CFGR2 JITOFF_D* renamed CKMODE (#77)
* F4: Missing RCC enable/reset bits for various peripherals (#80)
* USART updated for most families (#75)
* F4: Ethernet peripheral updates (#81, #87)
* F4: RCC updates (#83)

## v 0.3.2 2018-10-07
* F4: Update ethernet peripheral across entire family (#71, #73)

### Breaking Changes
* F4 ethernet MACMIIDR field TD is renamed MD to align with the reference
  manual

## v 0.3.1 fe63529 2018-10-07
* Fix typo in `tim16.yaml` that prevents builds on most devices

## v 0.3.0 241ca45 2018-10-07
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

Thanks to @ehntoo, @octronics, @burrbull, and @MattCatz for lots of work in
this release!

## v 0.2.3 c15e4a6 2018-09-07
* STM32F301: Fix incorrect aliasing of ADC.CSR and CCR
* STM32F4x9: Fix name of RM0386
* STM32F4: Improve timer coverage
* STM32F407: Include `TIM_OPM`
* Update to latest cortex-m-rt 0.6

## v 0.2.2 e648dae 2018-07-11
* Released crates now built with Form (#19, #29)
* Add a selection of documentation targets for docs.rs (#3)
* Many families: Add High/Low enum values for IDR/ODR on gpio_v2 (6c30cdc)
* Many families: Set DMA LIFCR and HIFCR to write-only (128b3d4)
* STM32F42{7,9}: Fix incorrect BWTR{3,4} (86dd104)
* STM32H7x3: Rename Flash->FLASH and fix PRAR_PRG2 (1e61674)
* STM32F7x{5,7,8,9}: Add PLLSAIRDY and PLLSAION (#35)

## v 0.2.1 954966a 2018-07-02
* Add STM32L4x5 device (#28)
* Add PLLR field for STM32F7x7 (#30)
* Add missing interrupts for STM32F7 devices (#27)
* Add PWR peripheral to various devices
* Fix incorrect USART3EN (#34)
* Fix incorrect naming for STM32H7 (#26)

## v0.2.0 0c108b3 2018-06-12

* Changelog started
* Fix STM32H7x3 register naming (0c108b3)
* OS X compatibility
* Update cortex-m-rt to 0.5.1
* Update svd2rust to 0.13.1
* Fix nvicPrioBits being incorrect in many STM32s (de117ef)
* Add support for specifying interrupts and modifying CPU node
