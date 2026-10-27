---
name: BlissClub Last Mile Intelligence Dashboard
description: A Minimal-UI-Kit analytics console rendered in pastels for logistics decision intelligence.
colors:
  lav-50: "#F3F1FF"
  lav-100: "#E6E2FD"
  lav-200: "#D5CEFA"
  lav-400: "#A497EE"
  lav-600: "#5B4AC0"
  mint-50: "#E9F7EF"
  mint-100: "#D3EFDF"
  mint-200: "#B9E5CC"
  mint-400: "#86CFA6"
  mint-600: "#23744B"
  butter-50: "#FFF6E1"
  butter-100: "#FDEBC4"
  butter-200: "#FBDEA3"
  butter-400: "#F1C370"
  butter-600: "#80560C"
  peach-50: "#FDEEEA"
  peach-100: "#FADCD4"
  peach-200: "#F6C7BC"
  peach-400: "#EEA090"
  peach-600: "#A8433A"
  sky-50: "#E8F3FB"
  sky-100: "#D2E8F6"
  sky-200: "#B8DBF1"
  sky-400: "#89C0E4"
  sky-600: "#25658C"
  grey-100: "#F9FAFB"
  grey-200: "#F4F6F8"
  grey-300: "#DFE3E8"
  grey-400: "#C4CDD5"
  grey-500: "#919EAB"
  grey-600: "#637381"
  grey-700: "#454F5B"
  grey-800: "#1C252E"
  line: "rgba(145, 158, 171, 0.2)"
  canvas: "#FBFAFE"
  card: "#FFFFFF"
typography:
  display:
    fontFamily: "Barlow, DM Sans, system-ui, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 700
    lineHeight: 1.15
    fontFeature: "tnum"
  headline:
    fontFamily: "Barlow, DM Sans, system-ui, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  title:
    fontFamily: "DM Sans, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "1.06rem"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: "DM Sans, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "DM Sans, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
    lineHeight: 1
rounded:
  xs: "6px"
  sm: "10px"
  md: "12px"
  lg: "16px"
  full: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
components:
  stat-card:
    background: "linear-gradient(135deg, var(--t50), var(--t200))"
    rounded: "{rounded.lg}"
    padding: "24px"
  nav-item:
    textColor: "{colors.grey-600}"
    rounded: "{rounded.sm}"
    padding: "8px 12px 8px 16px"
    minHeight: "46px"
  nav-item-active:
    backgroundColor: "{colors.lav-50}"
    textColor: "{colors.lav-600}"
  table-head:
    backgroundColor: "{colors.grey-200}"
    textColor: "{colors.grey-600}"
    padding: "14px 16px"
---

# BlissClub Last Mile Design System

This design system mirrors the Minimal-UI-Kit pastel architecture:
- Refined pastel semantic color tokens (Lavender, Mint, Butter, Peach, Sky).
- Editorial typography pairing: **Barlow** (bold tabular displays and section headers) with **DM Sans** (clean, readable text and tables).
- Fixed 280px left navigation with brand mark, count chips, and nested subnav with progress steps.
- Interactive stepper navigation between parts of each assignment question.
- Full-bleed data tables with grey header bands and dashed separator borders.
