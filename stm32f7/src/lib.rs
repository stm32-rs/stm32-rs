//! Peripheral access API for STM32F7 microcontrollers
//! (generated using [svd2rust](https://github.com/rust-embedded/svd2rust)
//! 0.13.1)
//!
//! You can find an overview of the API here:
//! https://docs.rs/svd2rust/0.13.1/svd2rust/#peripheral-api
//!
//! For more details see the README here:
//! https://github.com/adamgreig/stm32-rs
//!
//! This crate supports all STM32F7 devices; for the complete list please
//! see:
//! https://github.com/adamgreig/stm32-rs/tree/master/STM32F7
//!
//! Due to doc build limitations, not all devices may be shown on docs.rs;
//! a representative few have been selected instead. For a complete list of
//! available registers and fields see: https://stm32.agg.io/rs

#![allow(non_camel_case_types)]
#![feature(const_fn)]
#![feature(try_from)]
#![no_std]

#![cfg_attr(feature = "rt", feature(global_asm))]
#![cfg_attr(feature = "rt", feature(use_extern_macros))]
#![cfg_attr(feature = "rt", feature(used))]

extern crate vcell;
extern crate bare_metal;
extern crate cortex_m;

#[cfg(feature = "rt")]
extern crate cortex_m_rt;

#[cfg(feature = "stm32f7x2")]
pub mod stm32f7x2;

#[cfg(feature = "stm32f7x3")]
pub mod stm32f7x3;

#[cfg(feature = "stm32f7x5")]
pub mod stm32f7x5;

#[cfg(feature = "stm32f7x6")]
pub mod stm32f7x6;

#[cfg(feature = "stm32f7x7")]
pub mod stm32f7x7;

#[cfg(feature = "stm32f7x9")]
pub mod stm32f7x9;

