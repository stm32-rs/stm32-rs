# Changelog

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
