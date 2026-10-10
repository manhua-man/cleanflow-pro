# -*- coding: utf-8 -*-
HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CleanFlow Pro - Windows 空间管家</title>
  <style>
    /* ==========================================================================
       Windows 11 Fluent 2 Consumer-Grade Tokens (App Studio Grounded)
       ========================================================================== */
    :root {
      /* Surface & Mica Layers - Windows 11 Fluent 2 Grounded */
      --bg-base: #0a0d13;
      --bg-mica: #11151f;
      --bg-surface: #151a24;
      --bg-card: #1c2230;
      --bg-card-hover: #232b3c;
      --bg-card-active: #181d28;
      --bg-acrylic: rgba(22, 27, 38, 0.88);

      /* Subtle Fills */
      --fill-subtle: rgba(255, 255, 255, 0.045);
      --fill-subtle-hover: rgba(255, 255, 255, 0.085);
      --fill-subtle-active: rgba(255, 255, 255, 0.055);

      /* Borders & Dividers */
      --stroke-card: rgba(255, 255, 255, 0.08);
      --stroke-card-hover: rgba(0, 120, 212, 0.42);
      --stroke-divider: rgba(255, 255, 255, 0.06);
      --stroke-focus: #0078d4;

      /* Typography - High DPI Windows Optical Sizing */
      --font-family: 'Segoe UI Variable Text', 'Segoe UI Variable Display', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'SF Pro Text', Roboto, 'PingFang SC', 'Microsoft YaHei UI', sans-serif;
      --font-display: 'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'Cascadia Code', 'Consolas', monospace;
      --text-primary: #ffffff;
      --text-secondary: #d4dbe8;
      --text-tertiary: #95a3b7;
      --text-disabled: #556277;

      /* Primary Brand & Accents */
      --accent-primary: #0078d4;
      --accent-hover: #1084d9;
      --accent-active: #006cbe;
      --accent-gradient: linear-gradient(135deg, #0078d4 0%, #0099ff 50%, #00c7ff 100%);
      --accent-subtle: rgba(0, 120, 212, 0.16);
      --accent-glow: rgba(0, 120, 212, 0.45);

      /* Semantic Badges */
      --status-safe: #22c55e;
      --status-safe-bg: rgba(34, 197, 94, 0.12);
      --status-safe-border: rgba(34, 197, 94, 0.28);

      --status-warn: #fbbf24;
      --status-warn-bg: rgba(251, 191, 36, 0.12);
      --status-warn-border: rgba(251, 191, 36, 0.28);

      --status-danger: #f43f5e;
      --status-danger-bg: rgba(244, 63, 94, 0.12);
      --status-danger-border: rgba(244, 63, 94, 0.28);

      --status-purple: #c084fc;
      --status-purple-bg: rgba(192, 132, 252, 0.12);
      --status-purple-border: rgba(192, 132, 252, 0.28);

      --status-cyan: #22d3ee;
      --status-cyan-bg: rgba(34, 211, 238, 0.12);
      --status-cyan-border: rgba(34, 211, 238, 0.28);

      /* Radii & Shadows */
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-pill: 9999px;
      --shadow-card: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 4px 18px rgba(0, 0, 0, 0.35);
      --shadow-glow: 0 8px 28px rgba(0, 120, 212, 0.45);
      --motion-spring: cubic-bezier(0.16, 1, 0.3, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-drag: none;
    }

    body {
      font-family: var(--font-family);
      background-color: var(--bg-base);
      color: var(--text-primary);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      font-size: 13px;
      line-height: 1.5;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.14);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.24);
    }

    /* ==========================================================================
       Window TitleBar (Windows 11 Custom TitleBar)
       ========================================================================== */
    .desktop-titlebar {
      height: 38px;
      background-color: var(--bg-mica);
      border-bottom: 1px solid var(--stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px 0 12px;
      -webkit-app-region: drag;
      z-index: 1000;
      flex-shrink: 0;
    }

    .titlebar-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      -webkit-app-region: no-drag;
    }

    .app-logo-box {
      width: 24px;
      height: 24px;
      border-radius: var(--radius-sm);
      background: linear-gradient(135deg, #0078d4, #00c7ff);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(0, 120, 212, 0.4);
    }

    .app-brand-title {
      font-size: 12.5px;
      font-weight: 600;
      letter-spacing: -0.2px;
      color: var(--text-primary);
    }

    .app-version-badge {
      font-size: 10.5px;
      font-weight: 600;
      padding: 1px 6px;
      border-radius: var(--radius-pill);
      background-color: var(--fill-subtle);
      border: 1px solid var(--stroke-card);
      color: var(--text-tertiary);
    }

    .titlebar-center {
      display: flex;
      align-items: center;
      gap: 8px;
      -webkit-app-region: no-drag;
    }

    .drive-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 3px 12px;
      border-radius: var(--radius-pill);
      background: var(--fill-subtle);
      border: 1px solid var(--stroke-card);
      font-size: 11.5px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 120ms ease;
    }

    .drive-pill:hover {
      background: var(--fill-subtle-hover);
      color: var(--text-primary);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .drive-pill.active {
      border-color: #60cdff;
      background: rgba(0, 120, 212, 0.18);
      color: #ffffff;
      font-weight: 600;
    }

    .drive-pill-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: var(--status-safe);
    }

    .titlebar-actions {
      display: flex;
      align-items: center;
      height: 100%;
      -webkit-app-region: no-drag;
    }

    .win-caption-btn {
      width: 44px;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      color: var(--text-secondary);
      cursor: pointer;
      transition: background-color 80ms ease, color 80ms ease;
    }

    .win-caption-btn:hover {
      background-color: var(--fill-subtle-hover);
      color: var(--text-primary);
    }

    .win-caption-btn.btn-close:hover {
      background-color: #c42b1c;
      color: #ffffff;
    }

    /* ==========================================================================
       App Body Layout: Sidebar + Canvas + Inspector
       ========================================================================== */
    .app-body {
      flex: 1;
      display: flex;
      overflow: hidden;
      background-color: var(--bg-base);
      position: relative;
    }

    /* NavigationView (Sidebar) */
    .desktop-navigation {
      width: 242px;
      background-color: var(--bg-mica);
      border-right: 1px solid var(--stroke-divider);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      padding: 12px 10px;
      justify-content: space-between;
    }

    .nav-group-title {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-tertiary);
      padding: 6px 12px 4px 12px;
      letter-spacing: 0.3px;
    }

    .nav-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      color: var(--text-secondary);
      font-size: 12.5px;
      cursor: pointer;
      transition: all 120ms ease;
      position: relative;
    }

    .nav-item:hover {
      background-color: var(--fill-subtle-hover);
      color: var(--text-primary);
    }

    .nav-item.active {
      background: linear-gradient(90deg, rgba(0, 120, 212, 0.18) 0%, rgba(0, 120, 212, 0.04) 100%);
      color: #ffffff;
      font-weight: 600;
    }

    .nav-item.active::before {
      content: "";
      position: absolute;
      left: 0;
      top: 6px;
      bottom: 6px;
      width: 3.5px;
      border-radius: 2px;
      background: var(--accent-gradient);
      box-shadow: 0 0 8px rgba(0, 120, 212, 0.6);
    }

    .nav-item-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .nav-badge {
      font-size: 11px;
      font-weight: 600;
      padding: 1px 7px;
      border-radius: var(--radius-pill);
      background: var(--fill-subtle);
      color: var(--text-tertiary);
      font-family: var(--font-mono);
      font-variant-numeric: tabular-nums;
    }

    .nav-item.active .nav-badge {
      background: var(--accent-subtle);
      color: #60cdff;
    }

    /* Content Canvas */
    .content-canvas {
      flex: 1;
      background: radial-gradient(circle at 45% 150px, rgba(0, 120, 212, 0.08), transparent 60%), var(--bg-surface);
      display: flex;
      flex-direction: row;
      overflow: hidden;
      position: relative;
    }

    .workspace-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 24px 28px 64px 28px;
      gap: 20px;
    }

    .workspace-pane {
      display: none;
      flex-direction: column;
      gap: 20px;
    }

    .workspace-pane.active {
      display: flex;
      animation: fluentPaneIn 180ms var(--motion-spring);
    }

    @keyframes fluentPaneIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Workspace Header */
    .workspace-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--stroke-divider);
      padding-bottom: 14px;
    }

    .workspace-title-box h1 {
      font-size: 19px;
      font-weight: 600;
      letter-spacing: -0.3px;
      color: var(--text-primary);
    }

    .workspace-title-box p {
      font-size: 12px;
      color: var(--text-tertiary);
      margin-top: 2px;
    }

    .workspace-controls {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* ==========================================================================
       Hero Consumer Space Visualizer (CleanMyMac / Raycast Grade)
       ========================================================================== */
    .consumer-hero-banner {
      background: linear-gradient(135deg, rgba(30, 37, 51, 0.82) 0%, rgba(20, 25, 36, 0.92) 100%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 28px;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.09), 0 6px 24px rgba(0, 0, 0, 0.38);
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(20px);
    }

    .consumer-hero-banner::before {
      content: "";
      position: absolute;
      top: -60px;
      right: -60px;
      width: 260px;
      height: 260px;
      background: radial-gradient(circle, rgba(0, 120, 212, 0.22), transparent 70%);
      pointer-events: none;
    }

    .hero-left {
      display: flex;
      align-items: center;
      gap: 24px;
    }

    /* Radial Gauge Circle with Ambient Halo */
    .hero-gauge-container {
      position: relative;
      width: 136px;
      height: 136px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .gauge-ambient-glow {
      position: absolute;
      width: 140px;
      height: 140px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0, 150, 255, 0.2) 0%, rgba(0, 229, 255, 0.04) 55%, transparent 72%);
      animation: gaugeHaloPulse 4s ease-in-out infinite alternate;
      pointer-events: none;
    }

    @keyframes gaugeHaloPulse {
      0% { transform: scale(0.92); opacity: 0.35; }
      100% { transform: scale(1.08); opacity: 0.75; }
    }

    .gauge-svg {
      width: 100%;
      height: 100%;
      transform: rotate(-90deg);
      filter: drop-shadow(0 2px 8px rgba(0, 170, 255, 0.35));
    }

    .gauge-bg {
      fill: none;
      stroke: rgba(255, 255, 255, 0.06);
      stroke-width: 9.5;
    }

    .gauge-fill {
      fill: none;
      stroke: url(#gaugeGradient);
      stroke-width: 9.5;
      stroke-linecap: round;
      stroke-dasharray: 440;
      stroke-dashoffset: 140;
      transition: stroke-dashoffset 800ms var(--motion-spring);
    }

    .gauge-center-content {
      position: absolute;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    .gauge-val-row {
      display: flex;
      align-items: baseline;
      gap: 2px;
      line-height: 1;
    }

    .gauge-value {
      font-size: 32px;
      font-weight: 700;
      letter-spacing: -1.2px;
      color: #ffffff;
      font-family: var(--font-display);
      font-variant-numeric: tabular-nums;
    }

    .gauge-unit {
      font-size: 13px;
      font-weight: 600;
      color: #60cdff;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .gauge-label {
      font-size: 11px;
      color: var(--text-tertiary);
      font-weight: 500;
      margin-top: 3px;
      letter-spacing: 0.2px;
    }

    .hero-info {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .hero-title {
      font-size: 18px;
      font-weight: 600;
      color: #ffffff;
      letter-spacing: -0.2px;
    }

    .hero-desc {
      font-size: 12.5px;
      color: var(--text-secondary);
      max-width: 480px;
      line-height: 1.5;
    }

    .hero-tags {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
    }

    .hero-right-actions {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 10px;
      flex-shrink: 0;
    }

    /* Consumer Primary CTA Button */
    .btn-hero-cta {
      position: relative;
      overflow: hidden;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 12px 24px;
      background: linear-gradient(135deg, #0078d4 0%, #0099ff 50%, #00c7ff 100%);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: var(--radius-md);
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(0, 120, 212, 0.48), inset 0 1px 0 rgba(255, 255, 255, 0.35);
      transition: all 180ms var(--motion-spring);
    }

    .btn-hero-cta::after {
      content: "";
      position: absolute;
      top: 0;
      left: -100%;
      width: 50%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.28), transparent);
      transform: skewX(-20deg);
      animation: ctaShimmerSweep 5s infinite;
      pointer-events: none;
    }

    @keyframes ctaShimmerSweep {
      0%, 75% { left: -100%; }
      90%, 100% { left: 160%; }
    }

    .btn-hero-cta:hover {
      background: linear-gradient(135deg, #1084d9 0%, #1aa3ff 50%, #20d4ff 100%);
      transform: translateY(-2px);
      box-shadow: 0 8px 28px rgba(0, 120, 212, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.45);
    }

    .btn-hero-cta:active {
      transform: scale(0.975);
      box-shadow: 0 2px 10px rgba(0, 120, 212, 0.4);
    }

    /* Generic Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 120ms ease;
      border: 1px solid transparent;
      outline: none;
    }

    .btn-secondary {
      background-color: var(--fill-subtle);
      border-color: var(--stroke-card);
      color: var(--text-primary);
    }

    .btn-secondary:hover {
      background-color: var(--fill-subtle-hover);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .btn-primary {
      background-color: var(--accent-primary);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 120, 212, 0.35);
    }

    .btn-primary:hover {
      background-color: var(--accent-hover);
    }

    .btn-danger {
      background-color: rgba(239, 68, 68, 0.15);
      color: var(--status-danger);
      border-color: var(--status-danger-border);
    }

    .btn-danger:hover {
      background-color: #ef4444;
      color: #ffffff;
    }

    /* ==========================================================================
       Consumer 6-Card Feature Grid (User-Grade App Layout)
       ========================================================================== */
    .consumer-cards-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }

    .feature-card {
      background: linear-gradient(180deg, rgba(30, 37, 51, 0.82) 0%, rgba(21, 26, 36, 0.92) 100%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      cursor: pointer;
      transition: all 180ms var(--motion-spring);
      position: relative;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.09), 0 4px 18px rgba(0, 0, 0, 0.32);
      backdrop-filter: blur(16px);
    }

    .feature-card:hover {
      background: linear-gradient(180deg, rgba(37, 46, 63, 0.9) 0%, rgba(26, 32, 45, 0.98) 100%);
      border-color: rgba(0, 120, 212, 0.42);
      transform: translateY(-3px);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.16), 0 12px 30px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(0, 120, 212, 0.25);
    }

    .feature-card:hover .card-icon-box {
      transform: scale(1.08);
    }

    .feature-card:hover .card-action-link svg {
      transform: translateX(3px);
    }

    .feature-card-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
    }

    .card-icon-box {
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .icon-box-cyan { background: var(--status-cyan-bg); color: var(--status-cyan); border: 1px solid var(--status-cyan-border); }
    .icon-box-green { background: var(--status-safe-bg); color: var(--status-safe); border: 1px solid var(--status-safe-border); }
    .icon-box-orange { background: var(--status-warn-bg); color: var(--status-warn); border: 1px solid var(--status-warn-border); }
    .icon-box-blue { background: rgba(0, 120, 212, 0.16); color: #60cdff; border: 1px solid rgba(0, 120, 212, 0.3); }
    .icon-box-purple { background: var(--status-purple-bg); color: var(--status-purple); border: 1px solid var(--status-purple-border); }
    .icon-box-red { background: var(--status-danger-bg); color: var(--status-danger); border: 1px solid var(--status-danger-border); }

    .feature-card-metric {
      font-family: var(--font-display);
      font-variant-numeric: tabular-nums;
      display: flex;
      align-items: baseline;
      gap: 3px;
    }

    .metric-num {
      font-size: 21px;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.02em;
    }

    .metric-unit {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-tertiary);
      text-transform: uppercase;
      letter-spacing: 0.02em;
    }

    .feature-card-body {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .card-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-primary);
    }

    .card-desc {
      font-size: 11.5px;
      color: var(--text-tertiary);
      line-height: 1.4;
    }

    .feature-card-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--stroke-divider);
      padding-top: 10px;
      margin-top: 2px;
    }

    .card-action-link {
      font-size: 11.5px;
      color: #60cdff;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* ==========================================================================
       Scheme 1: Multi-Category Spectrum Distribution Bar
       ========================================================================== */
    .spectrum-card {
      background: linear-gradient(135deg, rgba(22, 28, 40, 0.95) 0%, rgba(16, 21, 31, 0.95) 100%);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
    .spectrum-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .spectrum-title-tag {
      font-size: 11px;
      font-weight: 700;
      color: #60cdff;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    .spectrum-main-title {
      font-size: 14.5px;
      font-weight: 600;
      color: #ffffff;
      margin-top: 2px;
    }
    .spectrum-reclaim-badge {
      font-size: 11.5px;
      color: var(--text-tertiary);
      font-family: var(--font-mono);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--stroke-card);
      padding: 4px 10px;
      border-radius: 9999px;
    }
    .spectrum-bar-track {
      height: 24px;
      width: 100%;
      border-radius: 9999px;
      overflow: hidden;
      display: flex;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5);
    }
    .spectrum-segment {
      height: 100%;
      transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1), filter 0.2s ease;
      position: relative;
      cursor: pointer;
      border-right: 2px solid rgba(10, 13, 19, 0.85);
      box-sizing: border-box;
    }
    .spectrum-segment:last-child {
      border-right: none;
    }
    .spectrum-segment:hover {
      filter: brightness(1.3);
      z-index: 2;
      box-shadow: 0 0 12px currentColor;
    }
    .spectrum-legend-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
      font-size: 11.5px;
    }
    .spectrum-legend-item {
      display: flex;
      align-items: center;
      gap: 7px;
      color: var(--text-secondary);
      cursor: pointer;
      padding: 4px 12px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .spectrum-legend-item:hover {
      background: rgba(255, 255, 255, 0.09);
      border-color: rgba(255, 255, 255, 0.18);
      transform: translateY(-1px);
    }
    .spectrum-color-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    /* ==========================================================================
       Scheme 1: Full-Disk Giant Files Treemap Box Hierarchy
       ========================================================================== */
    .treemap-section {
      background: linear-gradient(135deg, rgba(20, 26, 38, 0.95) 0%, rgba(14, 18, 27, 0.98) 100%);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35);
    }
    .treemap-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .treemap-canvas-container {
      height: 320px;
      width: 100%;
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      grid-template-rows: repeat(6, 1fr);
      gap: 6px;
      padding: 6px;
      background: rgba(8, 11, 16, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: var(--radius-md);
      box-sizing: border-box;
      position: relative;
    }
    .treemap-cell {
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
      box-sizing: border-box;
      user-select: none;
      backdrop-filter: blur(12px);
    }
    .treemap-cell:hover {
      filter: brightness(1.28);
      transform: translateY(-2px);
      z-index: 10;
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.65);
    }
    .treemap-cell.active-selected {
      outline: 2px solid #60cdff;
      outline-offset: 1px;
    }
    .treemap-cell-top {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .treemap-cell-badge {
      display: inline-block;
      align-self: flex-start;
      font-size: 10.5px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      letter-spacing: 0.02em;
      white-space: nowrap;
    }
    .treemap-cell-name {
      font-weight: 700;
      font-size: 13.5px;
      color: #ffffff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 2px;
    }
    .treemap-cell-path {
      font-size: 10.5px;
      opacity: 0.75;
      font-family: var(--font-mono);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .treemap-cell-bottom {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      padding-top: 6px;
      margin-top: 6px;
      font-size: 11px;
    }
    .treemap-inspector-strip {
      background: rgba(14, 18, 28, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-sm);
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .treemap-inspector-row1 {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .treemap-inspector-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      overflow: hidden;
    }
    .treemap-inspector-row2 {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-top: 6px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 11.5px;
    }
    .status-dot-pulse {
      animation: statusPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes statusPulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* ==========================================================================
       High-Density DataGrid & Views
       ========================================================================== */
    .desktop-commandbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-md);
      padding: 8px 12px;
    }

    .commandbar-left {
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
    }

    .search-box {
      position: relative;
      display: flex;
      align-items: center;
    }

    .search-box input {
      background-color: var(--fill-subtle);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-sm);
      padding: 5px 10px 5px 28px;
      font-size: 12px;
      color: var(--text-primary);
      outline: none;
      width: 220px;
      transition: all 120ms ease;
    }

    .search-box input:focus {
      border-color: var(--stroke-focus);
      background-color: rgba(0, 0, 0, 0.25);
    }

    .search-icon {
      position: absolute;
      left: 8px;
      color: var(--text-tertiary);
      pointer-events: none;
    }

    .filter-tabs {
      display: flex;
      align-items: center;
      gap: 4px;
      background-color: rgba(0, 0, 0, 0.2);
      padding: 3px;
      border-radius: var(--radius-sm);
    }

    .filter-tab {
      padding: 3px 10px;
      border-radius: var(--radius-sm);
      font-size: 11.5px;
      color: var(--text-tertiary);
      cursor: pointer;
      transition: all 100ms ease;
    }

    .filter-tab:hover {
      background-color: var(--fill-subtle-hover);
      color: var(--text-primary);
    }

    .filter-tab.active {
      background-color: var(--fill-subtle-hover);
      color: var(--text-primary);
      font-weight: 600;
    }

    .tag-pill {
      display: inline-flex;
      align-items: center;
      padding: 1px 7px;
      border-radius: var(--radius-pill);
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 0.3px;
      margin-right: 6px;
      vertical-align: middle;
    }
    .tag-blue { background: rgba(96, 205, 255, 0.15); color: #60cdff; border: 1px solid rgba(96, 205, 255, 0.3); }
    .tag-green { background: rgba(108, 203, 95, 0.15); color: #6ccb5f; border: 1px solid rgba(108, 203, 95, 0.3); }
    .tag-purple { background: rgba(190, 140, 255, 0.15); color: #be8cff; border: 1px solid rgba(190, 140, 255, 0.3); }
    .tag-orange { background: rgba(255, 170, 70, 0.15); color: #ffaa46; border: 1px solid rgba(255, 170, 70, 0.3); }

    /* DataGrid */
    .data-grid-container {
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-md);
      overflow: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .data-grid {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      text-align: left;
    }

    .data-grid thead th {
      background-color: rgba(0, 0, 0, 0.25);
      color: var(--text-tertiary);
      font-weight: 600;
      padding: 8px 12px;
      border-bottom: 1px solid var(--stroke-divider);
      font-size: 11px;
      letter-spacing: 0.2px;
      position: sticky;
      top: 0;
      z-index: 5;
      white-space: nowrap;
    }

    .data-grid tbody tr {
      border-bottom: 1px solid rgba(255, 255, 255, 0.035);
      cursor: pointer;
      transition: background-color 80ms ease;
      height: 36px;
    }

    .data-grid tbody tr:hover {
      background-color: rgba(255, 255, 255, 0.04);
    }

    .data-grid tbody tr.selected {
      background-color: rgba(0, 120, 212, 0.16);
      border-left: 3px solid #0078d4;
    }

    .data-grid td {
      padding: 6px 12px;
      vertical-align: middle;
      white-space: nowrap;
    }

    .col-checkbox {
      width: 36px;
      text-align: center;
    }

    .path-text {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--text-tertiary);
      max-width: 320px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      display: block;
    }

    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 1px 8px;
      border-radius: var(--radius-pill);
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
    }

    .badge-safe { background: var(--status-safe-bg); color: var(--status-safe); border: 1px solid var(--status-safe-border); }
    .badge-junction { background: var(--status-purple-bg); color: var(--status-purple); border: 1px solid var(--status-purple-border); }
    .badge-warn { background: var(--status-warn-bg); color: var(--status-warn); border: 1px solid var(--status-warn-border); }
    .badge-danger { background: var(--status-danger-bg); color: var(--status-danger); border: 1px solid var(--status-danger-border); }
    .badge-openwith { background: rgba(96, 205, 255, 0.15); color: #60cdff; border: 1px solid rgba(96, 205, 255, 0.3); }

    /* Checkbox */
    input[type="checkbox"] {
      appearance: none;
      width: 16px;
      height: 16px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      background-color: var(--fill-subtle);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      vertical-align: middle;
      position: relative;
    }

    input[type="checkbox"]:checked {
      background-color: var(--accent-primary);
      border-color: var(--accent-primary);
    }

    input[type="checkbox"]:checked::after {
      content: "";
      width: 4px;
      height: 7px;
      border: solid #ffffff;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
      position: absolute;
      top: 1px;
    }

    /* ==========================================================================
       Master-Detail Inspector Panel (Right Drawer)
       ========================================================================== */
    .desktop-inspector {
      width: 340px;
      background-color: var(--bg-mica);
      border-left: 1px solid var(--stroke-divider);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      transition: width 200ms var(--motion-spring), opacity 200ms ease;
      overflow: hidden;
    }

    .desktop-inspector.collapsed {
      width: 0;
      border-left-width: 0;
      opacity: 0;
      pointer-events: none;
    }

    .inspector-header {
      height: 44px;
      border-bottom: 1px solid var(--stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      background-color: rgba(0, 0, 0, 0.15);
      flex-shrink: 0;
    }

    .inspector-title {
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .inspector-close-btn {
      background: transparent;
      border: none;
      color: var(--text-tertiary);
      cursor: pointer;
      padding: 4px;
      border-radius: var(--radius-sm);
    }

    .inspector-close-btn:hover {
      background-color: var(--fill-subtle-hover);
      color: var(--text-primary);
    }

    .inspector-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      overflow-y: auto;
      flex: 1;
    }

    .inspector-card {
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-md);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .inspector-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-tertiary);
    }

    .inspector-val {
      font-size: 12.5px;
      color: var(--text-primary);
      word-break: break-all;
    }

    .inspector-path-box {
      font-family: var(--font-mono);
      font-size: 11px;
      color: #60cdff;
      background: rgba(0, 0, 0, 0.25);
      padding: 8px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--stroke-card);
      word-break: break-all;
      line-height: 1.4;
    }

    .inspector-actions {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 6px;
    }

    /* ==========================================================================
       Bottom StatusBar
       ========================================================================== */
    .desktop-statusbar {
      height: 28px;
      background-color: var(--bg-mica);
      border-top: 1px solid var(--stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      font-size: 11.5px;
      color: var(--text-tertiary);
      flex-shrink: 0;
    }

    .statusbar-left, .statusbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .statusbar-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: var(--status-safe);
    }

    /* Floating Context Menu */
    .fluent-context-menu {
      position: fixed;
      z-index: 9999;
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card-hover);
      border-radius: var(--radius-md);
      padding: 4px;
      box-shadow: var(--shadow-card);
      display: none;
      flex-direction: column;
      min-width: 190px;
      backdrop-filter: blur(20px);
    }

    .fluent-context-menu.active {
      display: flex;
      animation: menuPop 100ms var(--motion-spring);
    }

    @keyframes menuPop {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }

    .context-menu-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 80ms ease;
    }

    .context-menu-item:hover {
      background-color: var(--fill-subtle-hover);
      color: var(--text-primary);
    }

    .context-menu-item.danger:hover {
      background-color: rgba(239, 68, 68, 0.2);
      color: #ff8888;
    }

    .context-divider {
      height: 1px;
      background-color: var(--stroke-divider);
      margin: 3px 0;
    }

    /* Toast */
    .toast-container {
      position: fixed;
      bottom: 40px;
      right: 24px;
      z-index: 10000;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }

    .toast-message {
      position: relative;
      overflow: hidden;
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card-hover);
      border-radius: var(--radius-sm);
      padding: 9px 16px;
      font-size: 12px;
      color: #ffffff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
      display: flex;
      align-items: center;
      gap: 10px;
      animation: toastIn 200ms var(--motion-spring);
    }

    .toast-message::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      height: 2px;
      background: var(--accent-gradient);
      width: 100%;
      animation: toastProgress 3.2s linear forwards;
    }

    @keyframes toastProgress {
      from { width: 100%; }
      to { width: 0%; }
    }

    /* Silky micro-interactions */
    .data-grid tbody tr {
      transition: background-color 0.15s ease;
    }
    .data-grid tbody tr:hover {
      background-color: rgba(255, 255, 255, 0.045);
    }
    .feature-card {
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .feature-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
      border-color: var(--stroke-card-hover);
    }
    .btn {
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn:active {
      transform: scale(0.97);
    }

    @keyframes toastIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Modal */
    .fluent-modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      z-index: 11000;
      display: none;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(4px);
    }

    .fluent-modal-overlay.active {
      display: flex;
    }

    .fluent-modal {
      width: 440px;
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card-hover);
      border-radius: var(--radius-lg);
      padding: 22px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .icon {
      width: 16px;
      height: 16px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .icon svg {
      width: 100%;
      height: 100%;
      fill: currentColor;
    }

    /* Spotlight Floating Bar (Listary Feature A: Alt+Space) */
    .spotlight-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.55);
      backdrop-filter: blur(8px);
      z-index: 12000;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding-top: 12vh;
    }
    .spotlight-bar {
      width: 680px;
      max-width: 92vw;
      background: rgba(28, 28, 34, 0.94);
      backdrop-filter: blur(36px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 14px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7), 0 0 1px 1px rgba(255, 255, 255, 0.12);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: spotlightFadeIn 150ms cubic-bezier(0.1, 0.9, 0.2, 1);
    }
    @keyframes spotlightFadeIn {
      from { opacity: 0; transform: translateY(-12px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .spotlight-input-row {
      display: flex;
      align-items: center;
      padding: 14px 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      gap: 12px;
    }
    .spotlight-search-icon {
      width: 20px;
      height: 20px;
      fill: #60cdff;
      flex-shrink: 0;
    }
    .spotlight-input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #ffffff;
      font-size: 15px;
      font-family: inherit;
      font-weight: 500;
    }
    .spotlight-input::placeholder {
      color: rgba(255, 255, 255, 0.35);
      font-size: 13.5px;
    }
    .spotlight-badges {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .spotlight-kbd {
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #c9d1d9;
      font-family: var(--font-mono);
    }
    .spotlight-results {
      max-height: 380px;
      overflow-y: auto;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .spotlight-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 120ms ease;
      user-select: none;
    }
    .spotlight-item:hover, .spotlight-item.selected {
      background: rgba(0, 120, 212, 0.28);
      border: 1px solid rgba(0, 153, 255, 0.4);
    }
    .spotlight-item-left {
      display: flex;
      align-items: center;
      gap: 10px;
      overflow: hidden;
      flex: 1;
    }
    .spotlight-item-name {
      font-size: 13px;
      font-weight: 600;
      color: #ffffff;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    .spotlight-item-path {
      font-size: 11px;
      color: var(--text-tertiary);
      font-family: var(--font-mono);
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
      max-width: 300px;
    }
    .spotlight-item-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .spotlight-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      background: rgba(0, 0, 0, 0.2);
      font-size: 11px;
      color: var(--text-tertiary);
    }

    /* Filter Chips Styles (Pills) */
    .spotlight-chips-row {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px 8px 14px;
      overflow-x: auto;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      background: rgba(0, 0, 0, 0.12);
    }
    .spotlight-chip {
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-secondary);
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      cursor: pointer;
      white-space: nowrap;
      transition: all 120ms ease;
      user-select: none;
    }
    .spotlight-chip:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
    }
    .spotlight-chip.active {
      background: #0078d4;
      color: #ffffff;
      border-color: #0099ff;
      font-weight: 600;
      box-shadow: 0 1px 4px rgba(0, 120, 212, 0.4);
    }

    /* Action Runner Item Styles */
    .action-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--stroke-card);
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 140ms ease;
    }
    .action-card:hover {
      background: rgba(0, 120, 212, 0.18);
      border-color: rgba(0, 153, 255, 0.45);
      transform: translateX(2px);
    }
    .action-card-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .action-card-icon {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.06);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .action-card-title {
      font-size: 13px;
      font-weight: 600;
      color: #fff;
    }
    .action-card-desc {
      font-size: 11px;
      color: var(--text-secondary);
      margin-top: 2px;
    }
  </style>
</head>
<body>

  <!-- 1. Windows 11 Fluent TitleBar -->
  <header class="desktop-titlebar">
    <div class="titlebar-brand">
      <div class="app-logo-box">
        <svg style="width:14px; height:14px; fill:#fff;" viewBox="0 0 24 24">
          <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
        </svg>
      </div>
      <span class="app-brand-title">CleanFlow Pro</span>
      <span class="app-version-badge">v0.4.0</span>
    </div>

    <!-- Drive Switcher Pills -->
    <div class="titlebar-center" id="diskSelectorContainer">
      <!-- Injected via JS -->
    </div>

    <!-- Window Caption Controls & Listary Extensions -->
    <div class="titlebar-actions">
      <button class="btn btn-secondary" style="padding: 2px 10px; font-size: 11px; margin-right: 8px; display: inline-flex; align-items: center; gap: 6px; border-radius: 12px; height: 26px;" onclick="openSpotlight()" title="呼出毫秒级极简微型悬浮搜索框 (快捷键: 双击 Ctrl 或 Alt+Space)">
        <svg style="width:12px; height:12px; fill:#60cdff;" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        <span>Spotlight (双击 Ctrl / Alt+Space)</span>
      </button>
      <div id="licenseStatusBadge" style="display: inline-flex; align-items: center; gap: 6px; font-size: 11px; padding: 2px 10px; background: rgba(96, 205, 255, 0.12); border: 1px solid rgba(96, 205, 255, 0.35); border-radius: 12px; color: #60cdff; margin-right: 8px; height: 26px; cursor: pointer; font-weight: 600;" onclick="openLicenseModal()" title="点击查看当前授权状态、开启 7 天 PRO 体验或激活终身版">
        <span style="background: #60cdff; color: #080b10; font-size: 9px; font-weight: 800; padding: 1px 4px; border-radius: 3px;" id="licenseTierTag">FREE</span>
        <span id="licenseStatusText">社区免费版</span>
      </div>
      <div id="daemonStatusPill" style="display: inline-flex; align-items: center; gap: 6px; font-size: 11px; padding: 2px 10px; background: rgba(0, 120, 212, 0.12); border: 1px solid rgba(0, 120, 212, 0.3); border-radius: 12px; color: #60cdff; margin-right: 12px; height: 26px; cursor: pointer;" onclick="loadDaemonStatus()" title="点击刷新 C: 盘容量与后台守护健康度">
        <span style="width: 6px; height: 6px; border-radius: 50%; background: #107c41; display: inline-block;" id="daemonStatusDot"></span>
        <span id="daemonStatusText">守护: 监听中</span>
      </div>
      <button class="win-caption-btn" onclick="minimizeWindow()" title="最小化">
        <svg style="width:10px; height:10px; fill:currentColor;" viewBox="0 0 10 10"><path d="M0 5h10v1H0z"/></svg>
      </button>
      <button class="win-caption-btn" onclick="maximizeWindow()" title="最大化">
        <svg style="width:10px; height:10px; fill:currentColor;" viewBox="0 0 10 10"><path d="M0 0v10h10V0H0zm9 9H1V1h8v8z"/></svg>
      </button>
      <button class="win-caption-btn btn-close" onclick="shutdownApp()" title="退出">
        <svg style="width:10px; height:10px; fill:currentColor;" viewBox="0 0 10 10"><path d="M1 0L0 1l4 4-4 4 1 1 4-4 4 4 1-1-4-4 4-4-1-1-4 4z"/></svg>
      </button>
    </div>
  </header>

  <!-- 2. Main App Body -->
  <div class="app-body">
    <!-- Left Navigation Bar -->
    <nav class="desktop-navigation">
      <div>
        <div class="nav-group-title">核心功能视窗</div>
        <ul class="nav-list">
          <li class="nav-item active" data-tab="clean" onclick="switchTab('clean')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
              <span>极速空间清理</span>
            </div>
            <span class="nav-badge" id="badgeClean">体检</span>
          </li>
          <li class="nav-item" data-tab="analyze" onclick="switchTab('analyze')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg></span>
              <span>空间透视与去重</span>
            </div>
            <span class="nav-badge" id="badgeAnalyze">89 项</span>
          </li>
          <li class="nav-item" data-tab="search" onclick="switchTab('search')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
              <span>全盘秒搜与资产</span>
            </div>
            <span class="nav-badge" id="badgeSearch" style="background: rgba(0, 199, 255, 0.15); color: #00c7ff;">第二支柱</span>
          </li>
          <li class="nav-item" data-tab="purge" onclick="switchTab('purge')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
              <span>残留与死链瘦身</span>
            </div>
            <span class="nav-badge" id="badgePurge">排查</span>
          </li>
          <li class="nav-item" data-tab="tools" onclick="switchTab('tools')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg></span>
              <span>深度极客工具箱</span>
            </div>
            <span class="nav-badge" id="badgeTools">高级</span>
          </li>
        </ul>
      </div>

      <!-- Sidebar Bottom Info -->
      <div style="background: rgba(0,0,0,0.28); border: 1px solid var(--stroke-card); border-radius: var(--radius-sm); padding: 10px 12px; font-size: 11px; display:flex; flex-direction:column; gap:6px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="color:var(--text-secondary); font-weight:600;">系统盘 (C:)</span>
          <span style="color:var(--status-safe); font-weight:600;" id="sbDriveFree">29.8 GB 可用</span>
        </div>
        <div style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; overflow:hidden;">
          <div id="sbDriveBarFill" style="width:70%; height:100%; background:linear-gradient(90deg, #0078d4, #00c7ff); border-radius:3px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:10.5px; color:var(--text-tertiary);">
          <span>健康度良好</span>
          <span id="sbDriveTotal">共 100.0 GB</span>
        </div>
      </div>
    </nav>

    <!-- Content Workspace -->
    <main class="content-canvas">
      <div class="workspace-wrapper">

        <!-- ======================================================== -->
        <!-- WORKSPACE 1: 极速空间清理 (Clean) -->
        <!-- ======================================================== -->
        <section class="workspace-pane active" id="pane-clean">
          <!-- Hero Banner with Radial Space Gauge -->
          <div class="consumer-hero-banner">
            <div class="hero-left">
              <div class="hero-gauge-container">
                <div class="gauge-ambient-glow"></div>
                <svg class="gauge-svg" viewBox="0 0 160 160">
                  <defs>
                    <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#0066cc" />
                      <stop offset="50%" stop-color="#00aaff" />
                      <stop offset="100%" stop-color="#00f2fe" />
                    </linearGradient>
                  </defs>
                  <circle class="gauge-bg" cx="80" cy="80" r="68"></circle>
                  <circle class="gauge-fill" id="heroGaugeCircle" cx="80" cy="80" r="68"></circle>
                </svg>
                <div class="gauge-center-content">
                  <div class="gauge-val-row">
                    <span class="gauge-value" id="heroReclaimNum">29.8</span>
                    <span class="gauge-unit">GB</span>
                  </div>
                  <span class="gauge-label">可释放空间</span>
                </div>
              </div>

              <div class="hero-info">
                <div class="hero-title" id="heroHeadline">空间健康体检完成 · 建议立即清理</div>
                <div class="hero-desc">
                  已聚合 Windows 临时文件、现代开发包管理器缓存及主流浏览器离线冗余，随时可一键无损回收。
                </div>
                <!-- Universal Status Pills -->
                <div style="display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap;">
                  <div class="system-status-pill" onclick="emptyRecycleBinNow()" title="全盘回收站状态" style="background: rgba(96, 205, 255, 0.12); border: 1px solid rgba(96, 205, 255, 0.3); border-radius: 9999px; padding: 4px 12px; font-size: 11px; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <span style="color: #60cdff; font-weight: 600;">回收站:</span>
                    <span style="color: #fff;" id="overviewRecycleBinSize">0 B</span>
                  </div>
                  <div class="badge-pill badge-safe">
                    <span class="icon" style="width:12px; height:12px;"><svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                    100% 安全清理项已就绪
                  </div>
                  <div id="winapp2StatusPill" class="badge-pill" style="background: rgba(147, 51, 234, 0.15); border: 1px solid rgba(147, 51, 234, 0.3); color: #c084fc; cursor: pointer;" onclick="checkWinApp2Rules()" title="点击查看 WinApp2 规则状态">
                    <span class="icon" style="width:12px; height:12px;"><svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l7.59-7.59L21 8l-9 9z"/></svg></span>
                    <span>WinApp2 社区规则: 兼容已激活 (支持 2000+ 软件)</span>
                  </div>
                  <div class="badge-pill badge-openwith">零后台常驻 · 本地原生引擎</div>
                </div>
              </div>
            </div>

            <div class="hero-right-actions">
              <button class="btn-hero-cta" onclick="executeCleanSelected()">
                <span class="icon" style="width:18px; height:18px;"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
                <span id="heroBtnCleanText">一键快速清理 (16 GB)</span>
              </button>
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" style="padding: 6px 14px;" onclick="runScan()">
                  <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                  <span>重新深度体检</span>
                </button>
                <button class="btn btn-secondary" style="padding: 6px 14px;" onclick="exportHealthReport()">
                  <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg></span>
                  <span>导出诊断报告</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Multi-Category Spectrum Distribution Bar (Scheme 1 Component A) -->
          <div class="spectrum-card" id="cleanSpectrumCard" style="margin-top: 18px; margin-bottom: 20px;">
            <div class="spectrum-header">
              <div>
                <span class="spectrum-title-tag">系统空间多维资产构成光谱</span>
                <div class="spectrum-main-title">
                  <span id="spectrumDriveLabel">C 盘</span> <span id="spectrumTotalText" style="color: #60cdff;">14.5 GB</span> 可清理资产色彩编码分布
                </div>
              </div>
              <div class="spectrum-reclaim-badge">
                总计可回收: <strong id="spectrumReclaimVal" style="color: #22c55e;">14.5 GB</strong> / 100% 安全
              </div>
            </div>

            <!-- The Spectrum Bar -->
            <div class="spectrum-bar-track" id="spectrumSegmentsBar">
              <div style="width: 100%; height: 100%; background: rgba(255,255,255,0.06); display: flex; align-items: center; justify-content: center; font-size: 11px; color: var(--text-tertiary);">
                正在检索多维资产色彩分布...
              </div>
            </div>

            <!-- Spectrum Legend -->
            <div class="spectrum-legend-grid" id="spectrumLegendGrid">
            </div>
          </div>

          <!-- 6 Consumer Feature Cards Grid -->
          <div class="consumer-cards-grid" style="grid-template-columns: repeat(3, 1fr);">
            <!-- Card 1: System Temp -->
            <div class="feature-card" onclick="openInspectorByCategory('system')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-cyan">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardSystemMetric"><span class="metric-num">4.8</span><span class="metric-unit">GB</span></div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">系统冗余与临时垃圾</div>
                <div class="card-desc">用户临时目录、Windows 补丁下载及崩溃转储文件</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">完全安全可清</span>
                <span class="card-action-link"><span>查看详情</span><svg style="width:12px; height:12px; fill:currentColor;" viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg></span>
              </div>
            </div>

            <!-- Card 2: Dev Cache -->
            <div class="feature-card" onclick="openInspectorByCategory('dev_cache')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-green">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardDevMetric"><span class="metric-num">5.3</span><span class="metric-unit">GB</span></div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">现代开发与设计套件</div>
                <div class="card-desc">JetBrains/Android Studio、Cursor、Pip、Cargo、Adobe 及 npm/Unity 缓存</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">可安全回收</span>
                <span class="card-action-link"><span>管理缓存</span><svg style="width:12px; height:12px; fill:currentColor;" viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg></span>
              </div>
            </div>

            <!-- Card 3: Office & Social -->
            <div class="feature-card" onclick="openInspectorByCategory('office_chat')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-purple">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardOfficeMetric"><span class="metric-num">1.5</span><span class="metric-unit">GB</span></div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">微信与办公深度专清</div>
                <div class="card-desc">微信 4.0 日志、月度离线多媒体、旧版 XPlugin 与飞书缓存</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">聊天记录无损</span>
                <span class="card-action-link"><span>立即专清</span><svg style="width:12px; height:12px; fill:currentColor;" viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg></span>
              </div>
            </div>

            <!-- Card 4: Browser Cache -->
            <div class="feature-card" onclick="openInspectorByCategory('browser_cache')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-orange">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardBrowserMetric"><span class="metric-num">912.7</span><span class="metric-unit">MB</span></div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">主流浏览器深度专清</div>
                <div class="card-desc">Edge、Chrome 离线网络媒体与 IndexedDB 冗余数据</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">历史记录保留</span>
                <span class="card-action-link"><span>深度清理</span><svg style="width:12px; height:12px; fill:currentColor;" viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg></span>
              </div>
            </div>

            <!-- Card 5: Recycle Bin -->
            <div class="feature-card" style="cursor: default;">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-blue">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardRecycleBinMetric"><span class="metric-num">0</span><span class="metric-unit">B</span></div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">全盘回收站深度清空</div>
                <div class="card-desc">跨所有本地 NTFS 盘符彻底清空回收站历史删除文件</div>
              </div>
              <div class="feature-card-footer" style="padding-top: 8px;">
                <button class="btn btn-secondary" style="width: 100%; justify-content: center; padding: 4px 10px; font-size: 11px;" onclick="emptyRecycleBinNow()">
                  <span>立即清空回收站</span>
                </button>
              </div>
            </div>

            <!-- Card 6: Empty Folders -->
            <div class="feature-card" style="cursor: default;">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-purple">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                </div>
                <div class="feature-card-metric"><span class="metric-num" id="cardEmptyDirsMetric">0</span><span class="metric-unit">目录</span></div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">孤立幽灵空目录清理</div>
                <div class="card-desc">扫描 Temp 及应用目录下 0 字节无文件孤立壳文件夹</div>
              </div>
              <div class="feature-card-footer" style="padding-top: 8px; display: flex; gap: 6px;">
                <button class="btn btn-secondary" style="flex: 1; justify-content: center; padding: 4px 8px; font-size: 11px;" onclick="scanEmptyDirs()">
                  <span>排查</span>
                </button>
                <button class="btn btn-primary" style="flex: 1; justify-content: center; padding: 4px 8px; font-size: 11px;" onclick="cleanEmptyDirs()">
                  <span>清除</span>
                </button>
              </div>
            </div>
          </div>
        </section>


        <!-- ======================================================== -->
        <!-- WORKSPACE 2: 空间透视与去重 (Analyze) -->
        <!-- ======================================================== -->
        <section class="workspace-pane" id="pane-analyze">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>全盘空间透视与去重</h1>
              <p>排查全盘巨型沉淀大文件与双阶段 MD5 重复副本，定位隐蔽空间大户</p>
            </div>
            <div class="workspace-controls">
              <div class="filter-tabs" id="analyzeFilterTabs" style="margin: 0;">
                <div class="filter-tab active" onclick="setAnalyzeSubView('giant', this)">大文件全盘雷达 (<span id="analyzeGiantCount">89</span>)</div>
                <div class="filter-tab" onclick="setAnalyzeSubView('duplicates', this)">重复文件智选去重</div>
              </div>
            </div>
          </div>

          <!-- Subview 1: Giant Files Radar -->
          <div id="subviewGiantFiles" style="display: flex; flex-direction: column; gap: 14px; flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div style="font-size: 12px; color: var(--text-secondary);">
                当前识别到全盘大于 100 MB 的巨型文件资产，可定位所在目录或安全移除：
              </div>
              <button class="btn btn-secondary" onclick="loadGiantFiles()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>刷新大文件</span>
              </button>
            </div>

            <!-- Treemap Visualization Section (Scheme 1 Component B) -->
            <div class="treemap-section" id="giantTreemapSection">
              <div class="treemap-header">
                <div>
                  <span style="font-size: 11px; font-weight: 700; color: #10b981; letter-spacing: 0.05em; text-transform: uppercase;">巨型资产透视 · Treemap 空间矩形树图</span>
                  <div style="font-size: 14px; font-weight: 600; color: #fff; margin-top: 2px;">
                    全盘大资产面积直观透视 (<span id="treemapSubtitleCount">0</span> 处核心文件，色块面积 = 物理占用)
                  </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <span class="badge-pill badge-openwith" style="font-size: 11px;">鼠标悬停可透视并快速定位</span>
                </div>
              </div>

              <!-- Treemap Canvas -->
              <div class="treemap-canvas-container" id="giantTreemapCanvas">
                <div style="grid-column: span 12; grid-row: span 6; display: flex; align-items: center; justify-content: center; color: var(--text-tertiary); font-size: 13px;">
                  点击右上角“刷新大文件”开始构建全盘 Treemap 空间树图...
                </div>
              </div>

              <!-- Treemap Inspector Strip (2-Row Robust Layout) -->
              <div class="treemap-inspector-strip" id="treemapInspectorStrip">
                <div class="treemap-inspector-row1">
                  <div class="treemap-inspector-meta">
                    <span class="status-dot-pulse" style="width: 8px; height: 8px; border-radius: 50%; background: #60cdff; flex-shrink: 0;"></span>
                    <span style="font-weight: 600; font-size: 13.5px; color: #fff;" id="treemapDetailName">请悬停或选择上方树图色块</span>
                    <span class="tag-pill tag-blue" id="treemapDetailSize" style="font-family: var(--font-mono); font-weight: 700; padding: 2px 8px;">--</span>
                    <span class="tag-pill" id="treemapDetailCategory" style="background: rgba(255,255,255,0.08); color: #d4dbe8;">核心资产</span>
                  </div>
                  <div style="display: flex; gap: 8px; align-items: center;" id="treemapDetailActions">
                    <!-- Populated by JS -->
                  </div>
                </div>
                <div class="treemap-inspector-row2">
                  <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; color: var(--text-tertiary); font-family: var(--font-mono); font-size: 11px;">
                    <span style="color: #60cdff; font-weight: 600;">存储路径:</span> <span id="treemapDetailPath">--</span>
                  </div>
                  <div style="flex-shrink: 0; color: #10b981; font-weight: 500;" id="treemapDetailAdvice">
                    智能空间治理建议就绪
                  </div>
                </div>
              </div>
            </div>

            <div class="data-grid-container" style="flex: 1;">
              <table class="data-grid">
                <thead>
                  <tr>
                    <th style="width: 260px;">文件名称</th>
                    <th>物理存储路径</th>
                    <th style="width: 130px; text-align: right;">文件体积</th>
                    <th style="width: 140px; text-align: center;">最后修改时间</th>
                    <th style="width: 140px; text-align: center;">操作</th>
                  </tr>
                </thead>
                <tbody id="giantFilesTableBody"></tbody>
              </table>
            </div>
          </div>

          <!-- Subview 2: Duplicate Files Finder -->
          <div id="subviewDuplicates" style="display: none; flex-direction: column; gap: 14px; flex: 1;">
            <div style="background: var(--bg-card); border: 1px solid var(--stroke-card); border-radius: var(--radius-md); padding: 14px 16px; display: flex; flex-direction: column; gap: 10px;">
              <div style="display: flex; gap: 8px; align-items: center;">
                <span style="background: rgba(14, 165, 233, 0.15); color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3); padding: 3px 8px; border-radius: 4px; font-size: 11px; font-family: var(--font-mono); font-weight: 500;">BLAKE3 + 16KB Partial Hash 流式引擎</span>
                <span id="refsBlockCloneBadge" style="background: rgba(148, 163, 184, 0.12); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.25); padding: 3px 8px; border-radius: 4px; font-size: 11px; font-family: var(--font-mono);">卷特性: 待探测</span>
              </div>
              <div style="display: flex; gap: 12px; align-items: flex-end;">
                <div style="flex: 2;">
                  <label style="font-size: 11.5px; color: var(--text-secondary); display: block; margin-bottom: 5px;">排查目标路径</label>
                  <input type="text" id="dupScanPathInput" value="C:\\Users\\EDY\\Downloads" style="width: 100%; background: var(--fill-subtle); border: 1px solid var(--stroke-card); border-radius: var(--radius-sm); padding: 6px 10px; color: #fff; font-size: 12px; outline: none; font-family: var(--font-mono);">
                </div>
                <div style="flex: 1;">
                  <label style="font-size: 11.5px; color: var(--text-secondary); display: block; margin-bottom: 5px;">最小文件阈值</label>
                  <select id="dupMinSizeSelect" style="width: 100%; background: var(--fill-subtle); border: 1px solid var(--stroke-card); border-radius: var(--radius-sm); padding: 6px 10px; color: #fff; font-size: 12px; outline: none;">
                    <option value="1">大于 1 MB</option>
                    <option value="10">大于 10 MB</option>
                    <option value="50">大于 50 MB</option>
                  </select>
                </div>
                <button class="btn btn-primary" style="height: 32px; padding: 0 16px;" onclick="runDuplicatesScan()">
                  <span>开始排查重复</span>
                </button>
                <button class="btn btn-danger" style="height: 32px; padding: 0 16px;" onclick="cleanSelectedDuplicates()">
                  <span id="btnCleanDupsText">一键去重清理</span>
                </button>
              </div>
            </div>

            <div class="data-grid-container" style="flex: 1;">
              <table class="data-grid">
                <thead>
                  <tr>
                    <th class="col-checkbox"><input type="checkbox" checked onchange="toggleSelectAllDups(this)"></th>
                    <th style="width: 260px;">文件哈希 / 特征组</th>
                    <th>物理存储路径</th>
                    <th style="width: 120px; text-align: right;">单个体积</th>
                    <th style="width: 140px; text-align: center;">去重建议</th>
                    <th style="width: 90px; text-align: center;">操作</th>
                  </tr>
                </thead>
                <tbody id="duplicatesTableBody"></tbody>
              </table>
            </div>
          </div>
        </section>


        <!-- ======================================================== -->
        <!-- WORKSPACE 2.5: 全盘秒搜与资产中枢 (Search & Asset Hub) -->
        <!-- ======================================================== -->
        <section class="workspace-pane" id="pane-search">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>全盘毫秒检索与资产中枢</h1>
              <p>NTFS MFT 纯流式直读 · fsearch 级 1-Edit 拼写容错纠错 · 检索与治理闭环 (Junction 迁移 / 块克隆 / 进程锁)</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="rebuildSearchIndexes()" id="btnRebuildSearch">
                <svg class="icon" viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
                <span>重建全盘索引</span>
              </button>
            </div>
          </div>

          <!-- Volume Status Pills -->
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 16px; background: var(--bg-card); border: 1px solid var(--stroke-card); border-radius: var(--radius-md); padding: 12px 16px;">
            <div style="display:flex; align-items:center; gap: 12px;" id="searchVolumePills">
              <span style="font-size: 12px; color: var(--text-secondary); font-weight:600;">索引卷状态:</span>
              <span class="badge-pill badge-safe">检测中...</span>
            </div>
            <div style="display:flex; align-items:center; gap: 8px; font-size: 12px; color: var(--text-tertiary);" id="searchLatencyStats">
              <span>平均检索耗时: ~1 ms</span>
            </div>
          </div>

          <!-- Search Sub-modes (MFT File Search vs Trigram Code Grep) -->
          <div class="filter-tabs" id="searchModeTabs" style="margin-bottom: 12px;">
            <div class="filter-tab active" id="tabModeFiles" onclick="setSearchSubMode('files', this)">全盘毫秒检索 (MFT &amp; 1-Edit 容错)</div>
            <div class="filter-tab" id="tabModeGrep" onclick="setSearchSubMode('grep', this)">Trigram 源码全文 Grep (sym: / grep:)</div>
          </div>

          <!-- Interactive Search Input Box -->
          <div style="position: relative; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; background: rgba(0,0,0,0.3); border: 1.5px solid var(--accent); border-radius: var(--radius-md); padding: 10px 16px; gap: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);">
              <svg style="width: 18px; height: 18px; fill: var(--accent);" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
              <input type="text" id="searchInputField" placeholder="输入文件名、目录，或输入过滤器如: cagro.toml、gh tokio、cmd:dir、ext:exe、size:>50mb (按 Ctrl+F 随时聚焦)" 
                style="flex: 1; background: transparent; border: none; outline: none; color: #fff; font-size: 14px; font-family: inherit;"
                oninput="onSearchInput(this.value)" onkeydown="handleSearchInputKeydown(event)">
              <span class="badge-pill badge-neutral" style="font-size: 10px; cursor: pointer;" onclick="clearSearchInput()">清空</span>
            </div>

            <!-- Consumer-Grade Type Filter Chips (Pills) -->
            <div class="spotlight-chips-row" id="mainSearchChipsRow" style="margin-top: 10px; border-radius: var(--radius-sm); border: 1px solid var(--stroke-card); padding: 6px 12px; background: rgba(0,0,0,0.18);">
              <span style="font-size: 11px; color: var(--text-tertiary); margin-right: 4px; display:flex; align-items:center;">类型过滤:</span>
              <span class="spotlight-chip active" data-cat="all" onclick="selectMainSearchCategory('all')">全部</span>
              <span class="spotlight-chip" data-cat="folder" onclick="selectMainSearchCategory('folder')">文件夹</span>
              <span class="spotlight-chip" data-cat="doc" onclick="selectMainSearchCategory('doc')">文档</span>
              <span class="spotlight-chip" data-cat="pic" onclick="selectMainSearchCategory('pic')">图片</span>
              <span class="spotlight-chip" data-cat="video" onclick="selectMainSearchCategory('video')">视频</span>
              <span class="spotlight-chip" data-cat="audio" onclick="selectMainSearchCategory('audio')">音频</span>
              <span class="spotlight-chip" data-cat="archive" onclick="selectMainSearchCategory('archive')">压缩包</span>
              <span class="spotlight-chip" data-cat="app" onclick="selectMainSearchCategory('app')">应用</span>
            </div>

            <!-- Quick Filter Presets: File Search -->
            <div id="searchPresetsFiles" style="display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap;">
              <span style="font-size: 11px; color: var(--text-tertiary); display: flex; align-items: center;">文件预设:</span>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('size:>50mb')">巨型文件 (&gt;50MB)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('ext:exe')">可执行文件 (ext:exe)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('ext:safetensors')">AI 权重 (safetensors)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('kind:dir in:C:\\Users')">用户目录 (kind:dir)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('cagro.toml')">容错演示 (cagro.toml)</button>
            </div>

            <!-- Quick Filter Presets: Pro & Dev Superpowers -->
            <div id="searchPresetsPro" style="display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; align-items: center;">
              <span style="font-size: 11px; color: #60cdff; font-weight: 600; display: flex; align-items: center;">PRO 穿透与降噪:</span>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('gh tokio')">GitHub 穿透 (gh tokio)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('cargo serde')">Cargo 穿透 (cargo serde)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('regex:^clean.*\\.rs$')">RegEx 检索 (regex:)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('cmd: dir /b')">终端指令 (cmd:)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('calc')">系统别名 (calc)</button>
              <button class="btn btn-secondary" id="btnToggleNoiseShield" style="padding: 2px 8px; font-size: 11px; color: #60cdff; border-color: rgba(96,205,255,0.4);" onclick="toggleDevNoiseShield()" title="屏蔽 node_modules, .git, target, .venv 等海量碎文件噪声">降噪盾牌: 已开启</button>
            </div>

            <!-- Quick Filter Presets: Trigram Grep -->
            <div id="searchPresetsGrep" style="display: none; gap: 8px; margin-top: 10px; flex-wrap: wrap;">
              <span style="font-size: 11px; color: var(--text-tertiary); display: flex; align-items: center;">代码检索预设:</span>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('grep:fn main')">入口函数 (fn main)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('grep:TrigramIndex')">3-Gram 索引类</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('grep:FSCTL_ENUM_USN_DATA')">USN/MFT 流式常数</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="applySearchPreset('sym:WinApp2Rule')">WinApp2 规则类型</button>
            </div>
          </div>

          <!-- Pro Launcher Instant Hit Card -->
          <div id="launcherHitContainer" style="display: none; margin-bottom: 12px;"></div>

          <!-- Search Results Table -->
          <div style="background: var(--bg-card); border: 1px solid var(--stroke-card); border-radius: var(--radius-md); overflow: hidden;">
            <div style="padding: 12px 16px; border-bottom: 1px solid var(--stroke-card); display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 13px; font-weight: 600; color: #fff;" id="searchResultsCountTitle">检索结果 (0 项)</span>
              <span style="font-size: 11px; color: var(--text-tertiary);" id="searchMatchHint">支持 1-edit 拼写容错纠错 · 点击表头即时排序</span>
            </div>
            <div style="max-height: 440px; overflow-y: auto;">
              <table class="fluent-table" style="width: 100%;">
                <thead id="searchResultsThead">
                  <tr>
                    <th style="width: 28%; cursor: pointer; user-select: none;" id="thSearchCol1" onclick="toggleSearchSort('name')" title="点击正逆序重排">文件 / 目录名</th>
                    <th style="width: 14%; cursor: pointer; user-select: none;" id="thSearchCol2" onclick="toggleSearchSort('quality')" title="点击正逆序重排">匹配质量</th>
                    <th style="width: 12%; cursor: pointer; user-select: none;" id="thSearchCol3" onclick="toggleSearchSort('size')" title="点击正逆序重排">大小</th>
                    <th style="width: 32%; cursor: pointer; user-select: none;" id="thSearchCol4" onclick="toggleSearchSort('path')" title="点击正逆序重排">完整路径</th>
                    <th style="width: 14%; text-align: right;" id="thSearchCol5">治理动作</th>
                  </tr>
                </thead>
                <tbody id="searchResultsTableBody">
                  <tr>
                    <td colspan="5" style="text-align: center; padding: 36px; color: var(--text-tertiary);">
                      请输入检索词或点击上方预设，体验 ~1ms 极速检索与治理动作
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>


        <!-- ======================================================== -->
        <!-- WORKSPACE 3: 残留与死链瘦身 (Purge) -->
        <!-- ======================================================== -->
        <section class="workspace-pane" id="pane-purge">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>残留与死链瘦身治理</h1>
              <p>专攻软件卸载后遗留在 AppData 的孤立无主残留，清除注册表幽灵死链与失效自启项</p>
            </div>
            <div class="workspace-controls">
              <div class="filter-tabs" id="purgeFilterTabs" style="margin: 0;">
                <div class="filter-tab active" onclick="setPurgeSubView('leftovers', this)">软件卸载孤立残留 (<span id="purgeLeftoversCountLabel">排查</span>)</div>
                <div class="filter-tab" onclick="setPurgeSubView('registry', this)">注册表死链与失效自启 (<span id="purgeRegistryCountLabel">198 处</span>)</div>
              </div>
            </div>
          </div>

          <!-- Subview 1: AppData Leftovers -->
          <div id="subviewLeftovers" style="display: flex; flex-direction: column; gap: 14px; flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div style="font-size: 12px; color: var(--text-secondary);">
                排查主程序已删除、但历史配置与缓存仍积聚在 AppData 的孤立遗留文件夹：
              </div>
              <button class="btn btn-primary" onclick="loadAppLeftovers()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>深度排查残留</span>
              </button>
            </div>

            <div class="data-grid-container" style="flex: 1;">
              <table class="data-grid">
                <thead>
                  <tr>
                    <th style="width: 220px;">残留文件夹</th>
                    <th>关联物理路径</th>
                    <th style="width: 120px; text-align: right;">占用体积</th>
                    <th style="width: 90px; text-align: right;">文件数</th>
                    <th style="width: 220px;">判定原因</th>
                    <th style="width: 120px; text-align: center;">操作</th>
                  </tr>
                </thead>
                <tbody id="appLeftoversTableBody"></tbody>
              </table>
            </div>
          </div>

          <!-- Subview 2: Registry Dead Links & Ghost Autoruns -->
          <div id="subviewRegistry" style="display: none; flex-direction: column; gap: 14px; flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div style="font-size: 12px; color: var(--text-secondary);">
                清除已卸载程序残留的 MUICache 冗余、失效 OpenWith 右键打开方式及文件丢失的失效自启项：
              </div>
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" onclick="loadRegistryIssues()">
                  <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                  <span>排查死链</span>
                </button>
                <button class="btn btn-primary" onclick="cleanSelectedRegistryIssues()">
                  <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
                  <span>一键修复清理</span>
                </button>
              </div>
            </div>

            <div class="data-grid-container" style="flex: 1;">
              <table class="data-grid">
                <thead>
                  <tr>
                    <th class="col-checkbox"><input type="checkbox" checked onchange="toggleSelectAllRegistry(this)"></th>
                    <th style="width: 140px;">残留类型</th>
                    <th style="width: 240px;">键名 / 文件名</th>
                    <th>失效注册表路径 / 引用位置</th>
                    <th style="width: 100px; text-align: center;">状态</th>
                  </tr>
                </thead>
                <tbody id="registryTableBody"></tbody>
              </table>
            </div>
          </div>
        </section>


        <!-- ======================================================== -->
        <!-- WORKSPACE 4: 深度极客工具箱 (Tools) -->
        <!-- ======================================================== -->
        <section class="workspace-pane" id="pane-tools">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>深度极客工具箱</h1>
              <p>底层虚拟化与物理收缩工具：Docker 镜像管理、NTFS Junction 目录搬家与 SQLite 数据库整理</p>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
            <!-- Tool Card 1: Docker Virtualization -->
            <div class="feature-card" style="cursor: default; padding: 20px;">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-blue" style="width:40px; height:40px;">
                  <svg style="width:22px; height:22px; fill:currentColor;" viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
                </div>
                <div class="feature-card-metric" id="dockerMetric"><span class="metric-num">0</span><span class="metric-unit">B</span></div>
              </div>
              <div class="feature-card-body" style="margin-top:12px;">
                <div class="card-title" style="font-size:14.5px;">Docker 虚拟镜像与 Buildx 治理</div>
                <div class="card-desc" style="font-size:11.5px; margin-top:4px;">清理容器层构建缓存、孤立网络卷及未使用的旧版镜像，释放虚拟磁盘空间</div>
              </div>
              <div style="margin-top: 16px; display:flex; flex-direction:column; gap:8px;">
                <button class="btn btn-secondary" style="width: 100%; justify-content: center; font-size:11.5px;" onclick="pruneDockerBuildCache()">
                  <span>清理构建缓存 (Buildx)</span>
                </button>
                <button class="btn btn-primary" style="width: 100%; justify-content: center; font-size:11.5px;" onclick="pruneDockerSystem()">
                  <span>全量系统瘦身 (docker prune)</span>
                </button>
              </div>
            </div>

            <!-- Tool Card 2: Junction Migration -->
            <div class="feature-card" style="cursor: default; padding: 20px;">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-purple" style="width:40px; height:40px;">
                  <svg style="width:22px; height:22px; fill:currentColor;" viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg>
                </div>
                <div class="feature-card-metric"><span class="metric-num" style="color:#c084fc;">Junction</span></div>
              </div>
              <div class="feature-card-body" style="margin-top:12px;">
                <div class="card-title" style="font-size:14.5px;">目录无损跨盘搬家 (Junction)</div>
                <div class="card-desc" style="font-size:11.5px; margin-top:4px;">基于 NTFS 符号链接透明转移 Android 模拟器、微信记录至 D/E 盘，系统无感</div>
              </div>
              <div style="margin-top: 16px;">
                <button class="btn btn-secondary" style="width: 100%; justify-content: center; font-size:11.5px;" onclick="openMigrationWizardModal()">
                  <span>启动目录搬家向导</span>
                </button>
              </div>
            </div>

            <!-- Tool Card 3: SQLite Vacuum -->
            <div class="feature-card" style="cursor: default; padding: 20px;">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-green" style="width:40px; height:40px;">
                  <svg style="width:22px; height:22px; fill:currentColor;" viewBox="0 0 24 24"><path d="M12 3C7.58 3 4 4.79 4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7c0-2.21-3.58-4-8-4zm0 2c3.87 0 6 1.5 6 2s-2.13 2-6 2-6-1.5-6-2 2.13-2 6-2zm0 14c-3.87 0-6-1.5-6-2v-1.85c1.47.78 3.61 1.25 6 1.25s4.53-.47 6-1.25V17c0 .5-2.13 2-6 2zm0-4c-3.87 0-6-1.5-6-2v-1.85c1.47.78 3.61 1.25 6 1.25s4.53-.47 6-1.25V13c0 .5-2.13 2-6 2z"/></svg>
                </div>
                <div class="feature-card-metric"><span class="metric-num" style="color:#6ccb5f;">VACUUM</span></div>
              </div>
              <div class="feature-card-body" style="margin-top:12px;">
                <div class="card-title" style="font-size:14.5px;">数据库碎片物理压缩 (SQLite)</div>
                <div class="card-desc" style="font-size:11.5px; margin-top:4px;">针对 Cursor / IDE 膨胀的 state.vscdb 进行原生数据页重排，物理缩小文件体积</div>
              </div>
              <div style="margin-top: 16px;">
                <button class="btn btn-secondary" style="width: 100%; justify-content: center; font-size:11.5px;" onclick="runVacuumCursor()">
                  <span>执行 state.vscdb 压缩</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Active Junctions List in Tools Workspace -->
          <div style="background: var(--bg-card); border: 1px solid var(--stroke-card); border-radius: var(--radius-md); padding: 16px; margin-top: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
              <span style="font-size: 13px; font-weight: 600; color: #fff;">当前已建立的 NTFS Junction 无感软链接</span>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="loadActiveJunctions()">刷新链接</button>
            </div>
            <div id="toolsJunctionList" style="font-size: 11.5px; color: var(--text-secondary);">
              正在检测系统活跃符号链接...
            </div>
          </div>
        </section>

      </div>
      <!-- Right Master-Detail Inspector Drawer -->
      <aside class="desktop-inspector collapsed" id="desktopInspector">
        <div class="inspector-header">
          <div class="inspector-title">
            <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
            <span>属性与进程安全检查</span>
          </div>
          <button class="inspector-close-btn" onclick="toggleInspector(false)" title="收起检查面板">
            <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>

        <div class="inspector-body">
          <div class="inspector-card">
            <span class="inspector-label">目标资产名称</span>
            <span class="inspector-val" id="inspName" style="font-weight:600; font-size:13px;">请选择一项进行检查</span>
            <div style="margin-top:4px;">
              <span class="badge-pill badge-safe" id="inspCategory">就绪</span>
            </div>
          </div>

          <div class="inspector-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="inspector-label">完整物理路径</span>
              <button class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" title="复制路径" onclick="copyInspectorPath()">
                <span class="icon" style="width:12px; height:12px;"><svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg></span>
                <span>复制</span>
              </button>
            </div>
            <div class="inspector-path-box" id="inspPath">-</div>
          </div>

          <div class="inspector-card">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
              <div>
                <span class="inspector-label">占用体积</span>
                <div class="inspector-val" id="inspSize" style="font-weight:600; font-family:var(--font-mono); margin-top:2px;">-</div>
              </div>
              <div>
                <span class="inspector-label">文件数量</span>
                <div class="inspector-val" id="inspFiles" style="margin-top:2px;">-</div>
              </div>
            </div>
          </div>

          <div class="inspector-card">
            <span class="inspector-label">进程互斥与占用检测</span>
            <div id="inspLockStatus" style="font-size:12px; color:var(--status-safe); margin-top:2px;">
              进程未锁定 · 100% 安全可处理
            </div>
          </div>

          <div class="inspector-actions">
            <button class="btn btn-secondary" onclick="revealCurrentInspectorPath()">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg></span>
              <span>在文件资源管理器中定位</span>
            </button>
            <button class="btn btn-danger" onclick="cleanCurrentInspectorItem()">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg></span>
              <span>安全清理 / 删除该项</span>
            </button>
          </div>
        </div>
      </aside>
    </main>
  </div>

  <!-- 3. Desktop Bottom StatusBar -->
  <footer class="desktop-statusbar">
    <div class="statusbar-left">
      <span class="statusbar-dot"></span>
      <span id="sbDiskDetails">驱动器: C: 盘 (85% 已用)</span>
    </div>
    <div class="statusbar-right">
      <span id="sbProgress">体检完成</span>
      <span>|</span>
      <span id="sbSelection">已选 0 项 (0 B)</span>
      <span>|</span>
      <span>Rust 原生内核 v0.4.0 · <span style="color:var(--status-safe);">零后台常驻</span></span>
    </div>
  </footer>

  <!-- 4. Floating Context Menu -->
  <div class="fluent-context-menu" id="desktopContextMenu">
    <div class="context-menu-item" onclick="onContextReveal()">
      <span class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg></span>
      <span>在资源管理器中定位</span>
    </div>
    <div class="context-menu-item" onclick="onContextInspect()">
      <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
      <span>在属性面板中查看详情</span>
    </div>
    <div class="context-menu-item" onclick="onContextCopyPath()">
      <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg></span>
      <span>复制绝对路径</span>
    </div>
    <div class="context-divider"></div>
    <div class="context-menu-item danger" onclick="onContextClean()">
      <span class="icon" style="color:var(--status-danger);"><svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg></span>
      <span style="color:var(--status-danger);">安全清理 / 删除此项</span>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Confirmation Modal -->
  <div class="fluent-modal-overlay" id="confirmModal">
    <div class="fluent-modal">
      <div style="font-size:15px; font-weight:600; color:#fff;" id="confirmModalTitle">操作确认</div>
      <div style="font-size:12.5px; color:var(--text-secondary); line-height:1.5;" id="confirmModalBody">确定要执行此项操作吗？</div>
      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:10px;">
        <button class="btn btn-secondary" onclick="closeConfirmModal()">取消</button>
        <button class="btn btn-primary" id="confirmModalOkBtn" onclick="onConfirmModalOk()">确认继续</button>
      </div>
    </div>
  </div>

  <!-- Migration Wizard Modal -->
  <div class="fluent-modal-overlay" id="migrationWizardModal">
    <div class="fluent-modal" style="width: 720px; max-width: 92vw;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:16px; font-weight:600; color:#fff;">目录无损跨盘搬家向导 (NTFS Junction)</span>
          <span class="badge-pill badge-openwith">系统透明软链接</span>
        </div>
        <button class="inspector-close-btn" onclick="closeMigrationWizardModal()">
          <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      </div>
      <div style="font-size:12px; color:var(--text-secondary); line-height:1.5; margin-bottom:14px;">
        通过底层 NTFS 虚拟化将占用 C 盘的大型资产完整搬移到机械盘或从盘（如 D:/E: 盘），原位建立硬核透明符号链接，所有软件无感运行。
      </div>

      <!-- Quick AI & Developer Presets (Pillar 1 Integration) -->
      <div style="margin-bottom:14px;">
        <div style="font-size:12px; font-weight:600; color:#fff; margin-bottom:6px;">推荐高价值搬迁预设 (点击一键填入)</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;" id="migrationPresetTags">
        </div>
      </div>

      <!-- Source Directory Input & Target Drive -->
      <div style="display:grid; grid-template-columns: 2fr 1fr; gap:12px; margin-bottom:14px;">
        <div>
          <label style="font-size:11.5px; color:var(--text-secondary); display:block; margin-bottom:4px;">源目录绝对路径 (C: 盘)</label>
          <div style="display:flex; gap:6px;">
            <input type="text" id="customMigrateSource" placeholder="例如: C:\Users\EDY\.ollama\models" style="flex:1; background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none; font-family:var(--font-mono);" oninput="onMigrateSourceInput()">
            <button class="btn btn-secondary" style="padding:4px 10px; font-size:11px;" onclick="analyzeCustomMigrationPath()">检测体积</button>
          </div>
        </div>
        <div>
          <label style="font-size:11.5px; color:var(--text-secondary); display:block; margin-bottom:4px;">搬迁目标驱动器</label>
          <select id="customMigrateTargetDrive" style="width:100%; background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none;">
          </select>
        </div>
      </div>

      <!-- Mutual-Exclusion Process Inspector & Path Status -->
      <div id="migratePathInspectionCard" style="background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:12px; margin-bottom:14px; font-size:12px;">
        <div style="color:var(--text-tertiary);">请输入待搬迁路径或点击上方预设开始健康检测...</div>
      </div>

      <!-- Migration Action & Progress Indicator -->
      <div id="migrationProgressContainer" style="display:none; margin-bottom:14px;">
        <div style="display:flex; justify-content:space-between; font-size:11.5px; color:var(--text-secondary); margin-bottom:4px;">
          <span id="migrationStatusLabel">正在极速多线程无缓存拷贝...</span>
          <span id="migrationPercentLabel" style="color:#60cdff; font-weight:600;">0%</span>
        </div>
        <div style="height:6px; background:rgba(255,255,255,0.08); border-radius:3px; overflow:hidden;">
          <div id="migrationProgressBar" style="height:100%; width:0%; background:linear-gradient(90deg, #0078d4, #00f2fe); transition:width 200ms ease;"></div>
        </div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--stroke-divider); padding-top:14px;">
        <span style="font-size:11.5px; color:var(--text-tertiary);">原子事务回滚保护 · 支持随时无损还原</span>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-secondary" onclick="closeMigrationWizardModal()">取消</button>
          <button class="btn btn-primary" id="startMigrationBtn" onclick="executeCustomMigration()">
            <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
            <span>开始无损搬迁</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Spotlight Floating Search Overlay (Listary Feature A: Alt+Space) -->
  <div id="spotlightOverlay" class="spotlight-overlay" style="display:none;" onclick="handleSpotlightOverlayClick(event)">
    <div class="spotlight-bar" onclick="event.stopPropagation()">
      <div class="spotlight-input-row">
        <svg class="spotlight-search-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        <input type="text" id="spotlightInput" class="spotlight-input" placeholder="极简秒搜: 输入名称、拼音首字母(如jsq/wx)、grep:代码，↑↓翻历史，Tab动作..." autocomplete="off" oninput="onSpotlightInput(this.value)" onkeydown="handleSpotlightKeydown(event)" />
        <div class="spotlight-badges">
          <span class="spotlight-kbd">双击 Ctrl / Alt+Space</span>
          <span class="spotlight-kbd">↑↓ 历史/选定</span>
          <span class="spotlight-kbd">Tab 动作</span>
          <span class="spotlight-kbd" style="cursor:pointer;" onclick="closeSpotlight()">Esc</span>
        </div>
      </div>
      <div class="spotlight-chips-row" id="spotlightChipsRow">
        <span class="spotlight-chip active" data-cat="all" onclick="selectSpotlightCategory('all')">全部</span>
        <span class="spotlight-chip" data-cat="folder" onclick="selectSpotlightCategory('folder')">文件夹</span>
        <span class="spotlight-chip" data-cat="doc" onclick="selectSpotlightCategory('doc')">文档</span>
        <span class="spotlight-chip" data-cat="pic" onclick="selectSpotlightCategory('pic')">图片</span>
        <span class="spotlight-chip" data-cat="video" onclick="selectSpotlightCategory('video')">视频</span>
        <span class="spotlight-chip" data-cat="audio" onclick="selectSpotlightCategory('audio')">音频</span>
        <span class="spotlight-chip" data-cat="archive" onclick="selectSpotlightCategory('archive')">压缩包</span>
        <span class="spotlight-chip" data-cat="app" onclick="selectSpotlightCategory('app')">应用</span>
      </div>
      <div id="spotlightResultsContainer" class="spotlight-results">
        <div style="padding: 24px; text-align: center; color: var(--text-tertiary); font-size: 13px;">输入关键词或拼音首字母即刻全盘毫秒检索 · 上下键选择 · 回车打开 · Tab 动作流水线</div>
      </div>
      <div class="spotlight-footer">
        <span id="spotlightStatusText">CleanFlow Pro Spotlight (对齐 Listary 悬浮搜索与即搜即走架构)</span>
        <div style="display:flex; gap:14px;">
          <span>[Enter] 打开/PRO直达</span>
          <span>[Tab] 动作抽屉</span>
          <span>[Ctrl+G] Quick Switch</span>
          <span>[Esc] 退出</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Smart Action Hub Modal (Contextual & Auto-Discovered) -->
  <div class="fluent-modal-overlay" id="actionRunnerModal">
    <div class="fluent-modal" style="width: 660px; max-width: 92vw;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <div style="background: #0078d4; color:#fff; font-size:11px; font-weight:700; padding:2px 6px; border-radius:4px;">智能动作</div>
          <span style="font-size:16px; font-weight:600; color:#fff;">智能动作中心 (Smart Action Hub)</span>
        </div>
        <button class="inspector-close-btn" onclick="closeActionRunnerModal()">
          <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      </div>

      <!-- Target Info & Sub-view Switcher -->
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; background:rgba(0,0,0,0.25); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:8px 12px;">
        <div style="font-size:12px; color:var(--text-secondary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:420px;">
          目标: <span id="actionRunnerTargetPath" style="font-family:var(--font-mono); color:#60cdff;"></span>
        </div>
        <div class="filter-tabs" style="padding:2px; font-size:11px;">
          <div class="filter-tab active" id="tabActionViewItems" onclick="switchActionHubTab('actions')">情境推荐动作</div>
          <div class="filter-tab" id="tabActionViewTools" onclick="switchActionHubTab('tools')">已嗅探本地工具</div>
        </div>
      </div>

      <!-- View 1: Action items list -->
      <div id="actionRunnerItemsContainer" style="display:flex; flex-direction:column; gap:8px; max-height:360px; overflow-y:auto; margin-bottom:16px;">
        <!-- Dynamically injected -->
      </div>

      <!-- View 2: Detected tools overview (Zero-config display) -->
      <div id="actionRunnerToolsContainer" style="display:none; flex-direction:column; gap:8px; max-height:360px; overflow-y:auto; margin-bottom:16px;">
        <!-- Injected via JS -->
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--stroke-divider); padding-top:12px;">
        <span style="font-size:11.5px; color:var(--text-tertiary);" id="actionRunnerHintText">按数字键 1-6 或点击卡片即刻执行</span>
        <button class="btn btn-secondary" onclick="closeActionRunnerModal()">关闭</button>
      </div>
    </div>
  </div>

  <!-- Licensing & Pro Upgrade Modal -->
  <div class="fluent-modal-overlay" id="licenseModal">
    <div class="fluent-modal" style="width: 620px; max-width: 92vw;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <div style="background:linear-gradient(135deg, #0078d4, #00c7ff); padding:4px 8px; border-radius:4px; font-weight:800; font-size:11px; color:#fff;">PRO</div>
          <span style="font-size:16px; font-weight:600; color:#fff;">关于与授权管理 (CleanFlow Pro)</span>
        </div>
        <button class="inspector-close-btn" onclick="closeLicenseModal()">
          <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      </div>

      <!-- Current Status Card -->
      <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--stroke-card); border-radius: var(--radius-md); padding: 14px 16px; margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:14px; font-weight:700; color:#fff;" id="licModalTierTitle">检测中...</span>
            <span class="badge-pill badge-neutral" id="licModalTierBadge">FREE</span>
          </div>
          <span style="font-size:11px; color:var(--text-tertiary); font-family:var(--font-mono);" id="licModalFingerprint">设备指纹: ----</span>
        </div>
        <div style="font-size:12px; color:var(--text-secondary); line-height:1.5;" id="licModalDescription">
          正在加载授权信息...
        </div>
      </div>

      <!-- Free Trial Banner -->
      <div id="licTrialBanner" style="background: linear-gradient(135deg, rgba(96,205,255,0.12), rgba(0,120,212,0.08)); border: 1px solid rgba(96,205,255,0.35); border-radius: var(--radius-md); padding: 12px 16px; margin-bottom: 14px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:13px; font-weight:700; color:#60cdff;">开启 7 天 PRO 全特权免费体验</div>
          <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">一键体验双击 Ctrl 唤醒、Quick Switch 穿透、ReFS 块克隆去重与代码 Grep</div>
        </div>
        <button class="btn btn-primary" onclick="startProTrialQuick()" style="white-space:nowrap; padding:4px 12px; font-size:12px;">立即开启</button>
      </div>

      <!-- Activation Code Form -->
      <div style="background: rgba(0,0,0,0.2); border: 1px solid var(--stroke-card); border-radius: var(--radius-md); padding: 14px 16px; margin-bottom: 16px;">
        <div style="font-size:12.5px; font-weight:600; color:#fff; margin-bottom:8px;">激活授权码</div>
        <div style="display:flex; gap:8px; margin-bottom:8px;">
          <input type="text" id="licInputName" placeholder="授权持有人 (如: 开发者姓名/团队名，选填)" style="flex:1; background:rgba(0,0,0,0.3); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none;" />
          <input type="text" id="licInputKey" placeholder="输入 25 位激活码或 Dev Key" style="flex:2; background:rgba(0,0,0,0.3); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none; font-family:var(--font-mono);" />
          <button class="btn btn-primary" onclick="submitLicenseActivation()" style="white-space:nowrap; padding:6px 14px; font-size:12px;">激活</button>
        </div>
        <div style="font-size:11px; color:var(--text-tertiary);">
          内置演示激活码: <code style="color:#60cdff; cursor:pointer;" onclick="document.getElementById('licInputKey').value='CFPRO-LIFETIME-2026-DEVMASTER-KEY'">CFPRO-LIFETIME-2026-DEVMASTER-KEY</code>
        </div>
      </div>

      <!-- Tier Comparison Matrix Preview -->
      <div style="border-top:1px solid var(--stroke-divider); padding-top:12px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:11px; color:var(--text-tertiary);">CleanFlow 坚持纯净克制理念 · 社区版永久免费 · PRO 版释放极客生产力</span>
        <button class="btn btn-secondary" onclick="closeLicenseModal()">关闭</button>
      </div>
    </div>
  </div>

  <script>
    // State Store
    const state = {
      currentDrive: 'C:',
      currentTab: 'overview',
      disks: [],
      scanReport: null,
      selectedPaths: new Set(),
      giantFiles: [],
      registryIssues: [],
      selectedRegistryIds: new Set(),
      registryFilterCategory: 'all',
      giantSizeFilter: 'all',
      inspectorTarget: null,
      contextTarget: null
    };

    function formatBytes(bytes) {
      if (!bytes || bytes === 0) return '0 B';
      const k = 1024;
      const dm = 1;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    function formatMetricHtml(bytes) {
      if (!bytes || bytes === 0) return '<span class="metric-num">0</span> <span class="metric-unit">B</span>';
      const k = 1024;
      const dm = 1;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      const val = parseFloat((bytes / Math.pow(k, i)).toFixed(dm));
      return `<span class="metric-num">${val}</span> <span class="metric-unit">${sizes[i]}</span>`;
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function showToast(msg) {
      const c = document.getElementById('toastContainer');
      const t = document.createElement('div');
      t.className = 'toast-message';
      t.innerHTML = `<span class="icon" style="color:#60cdff;"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span><span>${escapeHtml(msg)}</span>`;
      c.appendChild(t);
      setTimeout(() => { t.remove(); }, 3200);
    }

    
    // ==========================================
    // Universal Generic Modules State & Methods
    // ==========================================
    state.startupItems = [];
    state.installedApps = [];
    state.appLeftovers = [];
    state.emptyDirs = [];
    state.duplicateGroups = [];
    state.selectedDups = new Set();
    state.appsViewMode = 'installed';

    // 1. Startup Items
    async function loadStartupItems() {
      try {
        const res = await fetch('/api/startup/list');
        state.startupItems = await res.json();
        renderStartupTable();
      } catch (e) {
        showToast('加载自启项失败: ' + e.message);
      }
    }

    function renderStartupTable() {
      const tbody = document.getElementById('startupTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      let highCount = 0;
      let deadCount = 0;

      state.startupItems.forEach(item => {
        if (item.impact.includes('高影响')) highCount++;
        if (!item.exists) deadCount++;

        const tr = document.createElement('tr');
        const impactBadge = !item.exists 
          ? '<span class="tag-pill" style="background:rgba(255,255,255,0.1); color:#aaa;">失效死链</span>'
          : (item.impact.includes('高') ? '<span class="tag-pill" style="background:rgba(255,100,100,0.15); color:#ff6464; border:1px solid rgba(255,100,100,0.3);">高影响</span>'
          : (item.impact.includes('中') ? '<span class="tag-pill tag-blue">中等影响</span>'
          : '<span class="tag-pill tag-green">轻量启动</span>'));

        const statusText = item.exists 
          ? '<span style="color:var(--status-safe); font-size:11px;">正常</span>' 
          : '<span style="color:#ff6464; font-size:11px; font-weight:600;">文件丢失</span>';

        tr.innerHTML = `
          <td><span style="font-weight:600; color:#fff;">${escapeHtml(item.name)}</span></td>
          <td><span class="path-text" title="${escapeHtml(item.command)}">${escapeHtml(item.command)}</span></td>
          <td style="font-size:11px; color:var(--text-secondary);">${escapeHtml(item.source)}</td>
          <td style="text-align:center;">${impactBadge}</td>
          <td style="text-align:center;">${statusText}</td>
          <td style="text-align:center;">
            <button class="btn btn-danger" style="padding:2px 8px; font-size:11px;" onclick="removeStartupItem('${escapeHtml(item.source)}', '${escapeHtml(item.name)}', '${escapeHtml(item.location).replace(/\\/g, '\\\\')}')">移除</button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      if (document.getElementById('startupTotalMetric')) {
        document.getElementById('startupTotalMetric').innerHTML = `<span class="metric-num">${state.startupItems.length}</span><span class="metric-unit">项</span>`;
      }
      if (document.getElementById('startupHighImpactMetric')) {
        document.getElementById('startupHighImpactMetric').innerHTML = `<span class="metric-num" style="color:#ffaa46;">${highCount}</span><span class="metric-unit">项</span>`;
      }
      if (document.getElementById('startupDeadMetric')) {
        document.getElementById('startupDeadMetric').innerHTML = `<span class="metric-num" style="color:#6ccb5f;">${deadCount}</span><span class="metric-unit">项</span>`;
      }
      if (document.getElementById('badgeStartup')) {
        document.getElementById('badgeStartup').innerText = `${state.startupItems.length} 项`;
      }
      if (document.getElementById('overviewStartupCount')) {
        document.getElementById('overviewStartupCount').innerText = `${state.startupItems.length} 项常驻`;
      }
    }

    async function removeStartupItem(source, name, location) {
      openConfirmModal('移除自启动项', `确定要从系统启动列表中移除自启项 [${name}] 吗？`, async () => {
        closeConfirmModal();
        try {
          const res = await fetch('/api/startup/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source, name, location })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`已成功移除自启动项 [${name}]`);
            loadStartupItems();
          } else {
            showToast('移除失败: ' + (data.error || '未知错误'));
          }
        } catch (e) {
          showToast('请求异常: ' + e.message);
        }
      });
    }

    async function cleanDeadStartupItems() {
      const deadItems = state.startupItems.filter(i => !i.exists);
      if (deadItems.length === 0) {
        showToast('当前未发现失效死链自启项');
        return;
      }
      openConfirmModal('清理失效自启项', `共发现 ${deadItems.length} 个文件已丢失的失效启动项，确定一键清除吗？`, async () => {
        closeConfirmModal();
        let cleaned = 0;
        for (const item of deadItems) {
          try {
            await fetch('/api/startup/remove', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ source: item.source, name: item.name, location: item.location })
            });
            cleaned++;
          } catch(e) {}
        }
        showToast(`已清理 ${cleaned} 个失效死链`);
        loadStartupItems();
      });
    }

    // 2. Installed Apps & Leftovers
    async function loadInstalledApps() {
      try {
        const res = await fetch('/api/apps/list');
        state.installedApps = await res.json();
        renderAppsTable();
      } catch (e) {
        showToast('加载已装软件列表失败: ' + e.message);
      }
    }

    async function loadAppLeftovers() {
      try {
        showToast('正在排查卸载后残留数据...');
        const res = await fetch('/api/apps/leftovers');
        state.appLeftovers = await res.json();
        if (document.getElementById('leftoversCountLabel')) {
          document.getElementById('leftoversCountLabel').innerText = `${state.appLeftovers.length} 处`;
        }
        if (document.getElementById('purgeLeftoversCountLabel')) {
          document.getElementById('purgeLeftoversCountLabel').innerText = `${state.appLeftovers.length} 处`;
        }
        if (document.getElementById('badgePurge')) {
          document.getElementById('badgePurge').innerText = `${state.appLeftovers.length + state.registryIssues.length} 处`;
        }
        setAppsView('leftovers');
        renderLeftoversTable();
        showToast(`排查完成，发现 ${state.appLeftovers.length} 处疑似孤立数据残留`);
      } catch (e) {
        showToast('排查残留失败: ' + e.message);
      }
    }

    function setAppsView(mode, el) {
      state.appsViewMode = mode;
      document.querySelectorAll('#appsFilterTabs .filter-tab').forEach(t => t.classList.remove('active'));
      if (el) el.classList.add('active');
      else {
        const idx = mode === 'installed' ? 0 : 1;
        const tabs = document.querySelectorAll('#appsFilterTabs .filter-tab');
        if (tabs[idx]) tabs[idx].classList.add('active');
      }

      const tInst = document.getElementById('installedAppsTable');
      const tLeft = document.getElementById('appLeftoversTable');
      if (mode === 'installed') {
        if (tInst) tInst.style.display = 'table';
        if (tLeft) tLeft.style.display = 'none';
        renderAppsTable();
      } else {
        if (tInst) tInst.style.display = 'none';
        if (tLeft) tLeft.style.display = 'table';
        renderLeftoversTable();
      }
    }

    function filterAppsTable() {
      if (state.appsViewMode === 'installed') renderAppsTable();
      else renderLeftoversTable();
    }

    function renderAppsTable() {
      const tbody = document.getElementById('installedAppsTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const q = (document.getElementById('appsSearchInput')?.value || '').toLowerCase();

      state.installedApps.forEach(app => {
        if (q && !app.name.toLowerCase().includes(q) && !app.publisher.toLowerCase().includes(q)) return;

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span style="font-weight:600; color:#fff;">${escapeHtml(app.name)}</span></td>
          <td style="font-size:11px; color:var(--text-secondary);">${escapeHtml(app.version || '-')}</td>
          <td style="font-size:11px; color:var(--text-secondary);">${escapeHtml(app.publisher || '-')}</td>
          <td style="text-align:right; font-family:var(--font-mono); font-weight:600; color:#60cdff;">${app.size_bytes > 0 ? formatBytes(app.size_bytes) : '-'}</td>
          <td><span class="path-text" title="${escapeHtml(app.install_location)}">${escapeHtml(app.install_location || '-')}</span></td>
          <td style="text-align:center;">
            ${app.uninstall_string ? `<button class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="runUninstallApp('${escapeHtml(app.uninstall_string).replace(/\\/g, '\\\\')}')">卸载</button>` : '-'}
          </td>
        `;
        tbody.appendChild(tr);
      });

      if (document.getElementById('appsCountLabel')) {
        document.getElementById('appsCountLabel').innerText = state.installedApps.length;
      }
      if (document.getElementById('badgeApps')) {
        document.getElementById('badgeApps').innerText = `${state.installedApps.length} 款`;
      }
      if (document.getElementById('overviewAppsCount')) {
        document.getElementById('overviewAppsCount').innerText = `${state.installedApps.length} 款纳管`;
      }
    }

    function renderLeftoversTable() {
      const tbody = document.getElementById('appLeftoversTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const q = (document.getElementById('appsSearchInput')?.value || '').toLowerCase();

      state.appLeftovers.forEach(item => {
        if (q && !item.folder_name.toLowerCase().includes(q) && !item.path.toLowerCase().includes(q)) return;

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span style="font-weight:600; color:#ffaa46;">${escapeHtml(item.folder_name)}</span></td>
          <td><span class="path-text" title="${escapeHtml(item.path)}">${escapeHtml(item.path)}</span></td>
          <td style="text-align:right; font-family:var(--font-mono); font-weight:600; color:#60cdff;">${formatBytes(item.size_bytes)}</td>
          <td style="text-align:right; font-family:var(--font-mono); color:var(--text-tertiary);">${item.file_count}</td>
          <td style="font-size:11.5px; color:var(--text-secondary);">${escapeHtml(item.reason)}</td>
          <td style="text-align:center;">
            <button class="btn btn-danger" style="padding:2px 8px; font-size:11px;" onclick="cleanSingleLeftover('${escapeHtml(item.path).replace(/\\/g, '\\\\')}')">清理残留</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    async function runUninstallApp(uninstallString) {
      openConfirmModal('启动应用卸载向导', '即将调用该应用程序原生卸载向导，确认启动吗？', async () => {
        closeConfirmModal();
        try {
          const res = await fetch('/api/apps/uninstall', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ uninstall_string: uninstallString })
          });
          const data = await res.json();
          if (data.success) {
            showToast('已唤起官方卸载程序');
          } else {
            showToast('调用卸载程序失败: ' + (data.error || '未知错误'));
          }
        } catch(e) {
          showToast('异常: ' + e.message);
        }
      });
    }

    async function cleanSingleLeftover(path) {
      openConfirmModal('清理孤立数据残留', `即将删除遗留文件夹 ${path}，确认继续吗？`, async () => {
        closeConfirmModal();
        try {
          const res = await fetch('/api/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paths: [path] })
          });
          const data = await res.json();
          showToast(`已清理释放 ${formatBytes(data.bytes_freed)}`);
          loadAppLeftovers();
        } catch(e) {
          showToast('清理失败: ' + e.message);
        }
      });
    }

    // 3. System Universal Maintenance
    async function loadSystemMaintenance() {
      try {
        const res = await fetch('/api/system/maintenance');
        const data = await res.json();
        if (data && data.recycle_bin) {
          if (document.getElementById('maintRecycleBinMetric')) {
            document.getElementById('maintRecycleBinMetric').innerHTML = formatMetricHtml(data.recycle_bin.size_bytes);
          }
          if (document.getElementById('overviewRecycleBinSize')) {
            document.getElementById('overviewRecycleBinSize').innerText = formatBytes(data.recycle_bin.size_bytes);
          }
          if (document.getElementById('badgeSystemMaint')) {
            document.getElementById('badgeSystemMaint').innerText = formatBytes(data.recycle_bin.size_bytes);
          }
        }
      } catch (e) {
        showToast('获取系统维护状态失败: ' + e.message);
      }
    }

    async function emptyRecycleBinNow() {
      openConfirmModal('清空回收站确认', '即将清空全盘回收站中的所有文件，此操作不可撤销，确认清空吗？', async () => {
        closeConfirmModal();
        showToast('正在清空全盘回收站...');
        try {
          const res = await fetch('/api/system/recycle-bin/empty', { method: 'POST' });
          const data = await res.json();
          if (data.success) {
            showToast(`回收站已清空，释放 ${formatBytes(data.bytes_freed)} 空间`);
            loadSystemMaintenance();
            refreshDisks();
          } else {
            showToast('清空失败: ' + (data.error || '未知错误'));
          }
        } catch(e) {
          showToast('清空异常: ' + e.message);
        }
      });
    }

    async function flushDnsNow() {
      showToast('正在刷新本地 DNS 解析缓存...');
      try {
        const res = await fetch('/api/system/flush-dns', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
          showToast('本地 DNS 解析缓存已成功刷新！');
        } else {
          showToast('刷新 DNS 失败: ' + (data.error || '未知错误'));
        }
      } catch (e) {
        showToast('刷新异常: ' + e.message);
      }
    }

    async function scanEmptyDirs() {
      showToast('正在扫描临时目录中的孤立空目录...');
      try {
        const res = await fetch('/api/system/empty-dirs/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_dir: '' })
        });
        state.emptyDirs = await res.json();
        if (document.getElementById('emptyDirsCountLabel')) {
          document.getElementById('emptyDirsCountLabel').innerText = `${state.emptyDirs.length}`;
        }
        showToast(`扫描完毕，发现 ${state.emptyDirs.length} 个空目录`);
      } catch(e) {
        showToast('扫描空目录失败: ' + e.message);
      }
    }

    async function cleanEmptyDirs() {
      if (state.emptyDirs.length === 0) {
        showToast('当前未发现待清理的空目录，请先排查');
        return;
      }
      openConfirmModal('清理空目录', `即将安全移除 ${state.emptyDirs.length} 个 0 字节孤立空目录，确认继续吗？`, async () => {
        closeConfirmModal();
        try {
          const res = await fetch('/api/system/empty-dirs/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paths: state.emptyDirs })
          });
          const data = await res.json();
          showToast(`已成功移除 ${data.cleaned_count} 个空目录`);
          state.emptyDirs = [];
          if (document.getElementById('emptyDirsCountLabel')) {
            document.getElementById('emptyDirsCountLabel').innerText = '0';
          }
        } catch(e) {
          showToast('清理失败: ' + e.message);
        }
      });
    }

    // 4. Duplicate Files Finder
    async function runDuplicatesScan() {
      const pathInput = document.getElementById('dupScanPathInput');
      const minMb = parseInt(document.getElementById('dupMinSizeSelect')?.value || '1', 10);
      let targetDir = pathInput ? pathInput.value.trim() : '';

      showToast('正在进行 BLAKE3 流式特征哈希排查...');
      
      // Probe volume block clone capability
      try {
        const volRes = await fetch('/api/duplicates/volume-status', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: targetDir })
        });
        const volStatus = await volRes.json();
        const badge = document.getElementById('refsBlockCloneBadge');
        if (badge) {
          if (volStatus.supports_block_cloning) {
            badge.innerText = `${volStatus.file_system} Dev Drive (支持 ReFS 块克隆写时复制)`;
            badge.style.color = '#34d399';
            badge.style.background = 'rgba(16, 185, 129, 0.15)';
            badge.style.borderColor = 'rgba(16, 185, 129, 0.35)';
          } else {
            badge.innerText = `${volStatus.file_system} 卷 (标准母本保护 + 副本删除模式)`;
            badge.style.color = '#60cdff';
            badge.style.background = 'rgba(14, 165, 233, 0.12)';
            badge.style.borderColor = 'rgba(14, 165, 233, 0.25)';
          }
        }
      } catch(e) {}

      try {
        const res = await fetch('/api/duplicates/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_dir: targetDir, min_size_mb: minMb })
        });
        state.duplicateGroups = await res.json();
        renderDuplicatesTable();
        showToast(`排查完毕，发现 ${state.duplicateGroups.length} 组重复文件`);
      } catch(e) {
        showToast('排查失败: ' + e.message);
      }
    }

    function renderDuplicatesTable() {
      const tbody = document.getElementById('duplicatesTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      state.selectedDups.clear();

      let totalWasted = 0;

      state.duplicateGroups.forEach(grp => {
        totalWasted += grp.wasted_bytes;

        grp.files.forEach((f, idx) => {
          const tr = document.createElement('tr');
          const isRecKeep = f.is_recommended_keep;
          if (!isRecKeep) state.selectedDups.add(f.path);

          tr.innerHTML = `
            <td class="col-checkbox">
              <input type="checkbox" ${!isRecKeep ? 'checked' : ''} onchange="toggleDupFile('${escapeHtml(f.path)}', this.checked)">
            </td>
            <td><span style="font-family:var(--font-mono); font-size:11px; color:#aaa;">${grp.hash.substring(0, 16)}...</span></td>
            <td><span class="path-text" title="${escapeHtml(f.path)}">${escapeHtml(f.path)}</span></td>
            <td style="text-align:right; font-family:var(--font-mono); font-weight:600; color:#60cdff;">${formatBytes(f.size_bytes)}</td>
            <td style="text-align:center;">
              ${isRecKeep 
                ? '<span class="tag-pill tag-green">推荐保留</span>' 
                : '<span class="tag-pill tag-orange">冗余副本</span>'}
            </td>
            <td style="text-align:center;">
              <button class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="revealInExplorer('${escapeHtml(f.path)}')">定位</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });

      updateDuplicatesSelectionText();
    }

    function toggleDupFile(path, checked) {
      if (checked) state.selectedDups.add(path);
      else state.selectedDups.delete(path);
      updateDuplicatesSelectionText();
    }

    function toggleSelectAllDups(master) {
      const chk = master.checked;
      state.duplicateGroups.forEach(grp => {
        grp.files.forEach(f => {
          if (!f.is_recommended_keep) {
            if (chk) state.selectedDups.add(f.path);
            else state.selectedDups.delete(f.path);
          }
        });
      });
      renderDuplicatesTable();
    }

    function updateDuplicatesSelectionText() {
      const btnText = document.getElementById('btnCleanDupsText');
      if (btnText) {
        btnText.innerText = `一键去重清理 (${state.selectedDups.size} 项)`;
      }
    }

    async function cleanSelectedDuplicates() {
      if (state.selectedDups.size === 0) {
        showToast('请选择待清理的重复副本');
        return;
      }
      openConfirmModal('清理重复文件副本', `确定要彻底删除选中的 ${state.selectedDups.size} 个重复副本文件吗？`, async () => {
        closeConfirmModal();
        try {
          const res = await fetch('/api/duplicates/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paths: Array.from(state.selectedDups) })
          });
          const data = await res.json();
          showToast(`去重完成，释放 ${formatBytes(data.bytes_freed)} 空间`);
          runDuplicatesScan();
          refreshDisks();
        } catch(e) {
          showToast('清理失败: ' + e.message);
        }
      });
    }

    // ==========================================
    // Data Export Utilities (CSV & JSON)
    // ==========================================
    function downloadBlob(content, filename, mimeType) {
      const blob = new Blob([content], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 200);
      showToast(`已导出: ${filename}`);
    }

    function exportStartupToCsv() {
      if (!state.startupItems || state.startupItems.length === 0) {
        showToast('暂无自启动数据可导出');
        return;
      }
      const headers = ['名称', '启动命令', '注册源', '注册位置', '开机影响', '文件是否存在', '状态'];
      const rows = state.startupItems.map(item => [
        `"${(item.name || '').replace(/"/g, '""')}"`,
        `"${(item.command || '').replace(/"/g, '""')}"`,
        `"${(item.source || '').replace(/"/g, '""')}"`,
        `"${(item.location || '').replace(/"/g, '""')}"`,
        `"${(item.impact || '').replace(/"/g, '""')}"`,
        item.exists ? '正常' : '文件丢失',
        item.enabled ? '启用' : '禁用'
      ]);
      const csv = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n');
      downloadBlob(csv, `CleanFlow_自启动清单_${new Date().toISOString().slice(0, 10)}.csv`, 'text/csv;charset=utf-8;');
    }

    function exportAppsToCsv() {
      if (!state.installedApps || state.installedApps.length === 0) {
        showToast('暂无已装软件数据可导出');
        return;
      }
      const headers = ['软件名称', '版本', '发布厂商', '占用字节', '估算大小', '安装路径', '卸载命令'];
      const rows = state.installedApps.map(app => [
        `"${(app.name || '').replace(/"/g, '""')}"`,
        `"${(app.version || '').replace(/"/g, '""')}"`,
        `"${(app.publisher || '').replace(/"/g, '""')}"`,
        app.size_bytes || 0,
        `"${formatBytes(app.size_bytes || 0)}"`,
        `"${(app.install_location || '').replace(/"/g, '""')}"`,
        `"${(app.uninstall_string || '').replace(/"/g, '""')}"`
      ]);
      const csv = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n');
      downloadBlob(csv, `CleanFlow_已装软件资产清单_${new Date().toISOString().slice(0, 10)}.csv`, 'text/csv;charset=utf-8;');
    }

    function exportHealthReport() {
      const report = {
        generated_at: new Date().toISOString(),
        device: 'Windows PC (x86_64)',
        engine_version: 'CleanFlow Pro v0.4.0',
        summary: {
          total_reclaimable_bytes: state.scanResult ? state.scanResult.total_size_bytes : 0,
          total_reclaimable_formatted: formatBytes(state.scanResult ? state.scanResult.total_size_bytes : 0),
          startup_items_count: state.startupItems ? state.startupItems.length : 0,
          installed_apps_count: state.installedApps ? state.installedApps.length : 0,
        },
        categories: (state.scanResult && state.scanResult.categories ? state.scanResult.categories : []).map(cat => ({
          name: cat.name,
          risk_level: cat.risk_level,
          size_bytes: cat.total_size_bytes,
          size_formatted: formatBytes(cat.total_size_bytes),
          files_count: cat.total_files,
          rules: (cat.rules || []).map(r => ({
            name: r.name,
            size_bytes: r.total_size_bytes,
            size_formatted: formatBytes(r.total_size_bytes),
            paths: r.matched_paths
          }))
        }))
      };
      const json = JSON.stringify(report, null, 2);
      downloadBlob(json, `CleanFlow_健康体检报告_${new Date().toISOString().slice(0, 10)}.json`, 'application/json');
    }

    async function checkWinApp2Rules() {
      try {
        const res = await fetch('/api/winapp2/status');
        const data = await res.json();
        if (data.available) {
          showToast(`WinApp2 社区规则已就绪: 已解析 ${data.total_rules} 项规则，命中 ${data.detected_apps} 款已装应用`);
        } else {
          showToast('WinApp2 状态: ' + (data.error || '未就绪'));
        }
      } catch(e) {
        showToast('获取 WinApp2 状态失败: ' + e.message);
      }
    }

    // Tab Switching
    function switchTab(tabId) {
      state.currentTab = tabId;
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      const activeNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
      if (activeNav) activeNav.classList.add('active');

      document.querySelectorAll('.workspace-pane').forEach(el => el.classList.remove('active'));
      const targetPane = document.getElementById(`pane-${tabId}`);
      if (targetPane) targetPane.classList.add('active');

      toggleInspector(false);

      if (tabId === 'analyze') {
        if (state.giantFiles.length === 0) loadGiantFiles();
      }
      if (tabId === 'purge') {
        if (state.appLeftovers.length === 0) loadAppLeftovers();
      }
      if (tabId === 'tools') {
        loadDockerStatus();
        loadActiveJunctions();
      }
      if (tabId === 'search') {
        loadSearchVolumes();
        setTimeout(() => {
          const inp = document.getElementById('searchInputField');
          if (inp) {
            inp.focus();
            if (inp.value.trim().length > 0) executeDiskSearch(inp.value.trim());
          }
        }, 50);
      }
    }

    let currentSearchSubMode = 'files';

    function setSearchSubMode(mode, tabEl) {
      currentSearchSubMode = mode;
      document.querySelectorAll('#searchModeTabs .filter-tab').forEach(t => t.classList.remove('active'));
      if (tabEl) tabEl.classList.add('active');

      const pFiles = document.getElementById('searchPresetsFiles');
      const pGrep = document.getElementById('searchPresetsGrep');
      const inp = document.getElementById('searchInputField');
      const hint = document.getElementById('searchMatchHint');

      if (mode === 'grep') {
        if (pFiles) pFiles.style.display = 'none';
        if (pGrep) pGrep.style.display = 'flex';
        if (inp) inp.placeholder = '输入源码符号或关键字，如: fn main、TrigramIndex、sym:scan (支持 in:目录 过滤)';
        if (hint) hint.innerText = 'Trigram 3-Gram 倒排索引秒级全文匹配';
      } else {
        if (pFiles) pFiles.style.display = 'flex';
        if (pGrep) pGrep.style.display = 'none';
        if (inp) inp.placeholder = '输入文件名、目录，或输入过滤器如: cagro.toml、ext:exe、size:>50mb、in:C:\\Users (按 Ctrl+F 随时聚焦)';
        if (hint) hint.innerText = '支持 1-edit 拼写容错纠错';
      }

      if (inp && inp.value.trim()) {
        executeDiskSearch(inp.value.trim());
      }
    }

    let searchDebounceTimer = null;
    let mainSearchCurrentCategory = 'all';

    function selectMainSearchCategory(cat) {
      mainSearchCurrentCategory = cat;
      const chips = document.querySelectorAll('#mainSearchChipsRow .spotlight-chip');
      chips.forEach(c => {
        if (c.getAttribute('data-cat') === cat) {
          c.classList.add('active');
        } else {
          c.classList.remove('active');
        }
      });
      const inp = document.getElementById('searchInputField');
      const val = inp ? inp.value.trim() : '';
      executeDiskSearch(val);
    }

    function onSearchInput(val) {
      if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        executeDiskSearch(val.trim());
      }, 120);
    }

    function clearSearchInput() {
      const inp = document.getElementById('searchInputField');
      if (inp) {
        inp.value = '';
        inp.focus();
        mainSearchCurrentCategory = 'all';
        const chips = document.querySelectorAll('#mainSearchChipsRow .spotlight-chip');
        chips.forEach(c => {
          if (c.getAttribute('data-cat') === 'all') c.classList.add('active');
          else c.classList.remove('active');
        });
        executeDiskSearch('');
      }
    }

    function applySearchPreset(preset) {
      const inp = document.getElementById('searchInputField');
      if (inp) {
        inp.value = preset;
        inp.focus();
        if (preset.startsWith('grep:') || preset.startsWith('sym:')) {
          const tabGrep = document.getElementById('tabModeGrep');
          if (tabGrep && currentSearchSubMode !== 'grep') setSearchSubMode('grep', tabGrep);
        }
        executeDiskSearch(preset);
      }
    }

    async function loadSearchVolumes() {
      try {
        const res = await fetch('/api/search/volumes');
        if (!res.ok) return;
        const vols = await res.json();
        const pillsContainer = document.getElementById('searchVolumePills');
        if (!pillsContainer || !vols || vols.length === 0) return;
        
        pillsContainer.innerHTML = '<span style="font-size: 12px; color: var(--text-secondary); font-weight:600;">已就绪卷:</span>' + 
          vols.map(v => {
            const accelBadge = v.is_ntfs ? 'NTFS / MFT' : v.fs_type;
            return `<span class="badge-pill badge-safe">${v.drive_letter}: [${v.label || '系统卷'}] · ${accelBadge}</span>`;
          }).join('');
      } catch(e) {
        console.warn('加载检索卷状态失败:', e);
      }
    }

    async function rebuildSearchIndexes() {
      const btn = document.getElementById('btnRebuildSearch');
      if (btn) btn.disabled = true;
      showToast('正在重新构建全盘 MFT / 文件索引缓存...');
      try {
        const res = await fetch('/api/search/rebuild', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
          showToast(`全盘索引重建成功！累计索引 ${data.total_indexed_entries} 项 (${data.volumes_count} 个卷)`);
          const inp = document.getElementById('searchInputField');
          if (inp && inp.value.trim()) executeDiskSearch(inp.value.trim());
        }
      } catch(e) {
        showToast('重建全盘索引失败: ' + e.message);
      } finally {
        if (btn) btn.disabled = false;
      }
    }

    let currentSearchHits = [];
    let currentSearchGrepMode = false;
    let currentSearchSort = { col: null, asc: true };
    let devNoiseShieldEnabled = true;
    let currentLauncherHit = null;

    function toggleDevNoiseShield() {
      devNoiseShieldEnabled = !devNoiseShieldEnabled;
      const btn = document.getElementById('btnToggleNoiseShield');
      if (btn) {
        if (devNoiseShieldEnabled) {
          btn.innerText = '降噪盾牌: 已开启';
          btn.style.color = '#60cdff';
          btn.style.borderColor = 'rgba(96,205,255,0.4)';
        } else {
          btn.innerText = '降噪盾牌: 已关闭 (含 node_modules)';
          btn.style.color = 'var(--text-tertiary)';
          btn.style.borderColor = 'var(--stroke-card)';
        }
      }
      const inp = document.getElementById('searchInputField');
      if (inp && inp.value.trim()) {
        executeDiskSearch(inp.value.trim());
      }
    }

    async function executeLauncherAction(actionType, target) {
      if (!actionType || !target) return;
      try {
        const res = await fetch('/api/launcher/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action_type: actionType, target: target })
        });
        const data = await res.json();
        if (data.success) {
          showToast(data.message || '已成功唤起动作');
          const ov = document.getElementById('spotlightOverlay');
          if (ov && ov.style.display !== 'none') {
            closeSpotlight();
          }
        } else {
          showToast('唤起失败: ' + (data.error || '未知错误'));
        }
      } catch (e) {
        showToast('执行异常: ' + e.message);
      }
    }

    function handleSearchInputKeydown(e) {
      if (e.key === 'Enter') {
        if (currentLauncherHit) {
          e.preventDefault();
          executeLauncherAction(currentLauncherHit.action_type, currentLauncherHit.target);
        }
      }
    }

    function toggleSearchSort(col) {
      if (currentSearchSort.col === col) {
        currentSearchSort.asc = !currentSearchSort.asc;
      } else {
        currentSearchSort.col = col;
        currentSearchSort.asc = true;
      }
      updateSearchSortHeaders();
      sortAndRenderSearchResults();
    }

    function updateSearchSortHeaders() {
      const colMap = {
        name: { id: 'thSearchCol1', text: currentSearchGrepMode ? '代码文件 : 行号' : '文件 / 目录名' },
        quality: { id: 'thSearchCol2', text: currentSearchGrepMode ? '匹配代码内容' : '匹配质量' },
        size: { id: 'thSearchCol3', text: currentSearchGrepMode ? '得分' : '大小' },
        path: { id: 'thSearchCol4', text: currentSearchGrepMode ? '完整文件路径' : '完整路径' },
      };
      for (const [k, v] of Object.entries(colMap)) {
        const el = document.getElementById(v.id);
        if (!el) continue;
        if (currentSearchSort.col === k) {
          el.innerText = `${v.text} ${currentSearchSort.asc ? '▲' : '▼'}`;
        } else {
          el.innerText = v.text;
        }
      }
    }

    function sortAndRenderSearchResults() {
      if (!currentSearchHits || currentSearchHits.length === 0) return;
      const { col, asc } = currentSearchSort;
      if (col) {
        currentSearchHits.sort((a, b) => {
          let cmp = 0;
          if (currentSearchGrepMode) {
            if (col === 'name') {
              const kA = `${a.file_name}:${a.line_number}`;
              const kB = `${b.file_name}:${b.line_number}`;
              cmp = kA.localeCompare(kB);
            } else if (col === 'quality') {
              cmp = (a.line_content || '').localeCompare(b.line_content || '');
            } else if (col === 'size') {
              cmp = (a.score || 0) - (b.score || 0);
            } else if (col === 'path') {
              cmp = (a.file_path || '').localeCompare(b.file_path || '');
            }
          } else {
            if (col === 'name') {
              cmp = (a.name || '').localeCompare(b.name || '');
            } else if (col === 'quality') {
              cmp = (a.score || 0) - (b.score || 0);
            } else if (col === 'size') {
              cmp = (a.size_bytes || 0) - (b.size_bytes || 0);
            } else if (col === 'path') {
              cmp = (a.path || '').localeCompare(b.path || '');
            }
          }
          return asc ? cmp : -cmp;
        });
      }
      renderSearchResultsTableRows();
    }

    function renderSearchResultsTableRows() {
      const tbody = document.getElementById('searchResultsTableBody');
      if (!tbody) return;
      if (!currentSearchHits || currentSearchHits.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 36px; color: var(--text-tertiary);">未找到匹配结果</td></tr>';
        return;
      }

      if (currentSearchGrepMode) {
        tbody.innerHTML = currentSearchHits.map(h => {
          const fileLoc = `${h.file_name}:${h.line_number}`;
          const fileIcon = '<svg style="width:14px;height:14px;fill:#60cdff;margin-right:6px;" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>';
          const lineSnippet = escapeHtml(h.line_content || '');
          const actionsHtml = `<button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapePath(h.file_path)}')">定位</button> <button class="btn btn-primary" style="padding: 2px 8px; font-size: 11px;" onclick="openActionRunnerModal('${escapePath(h.file_path)}', '${escapeHtml(h.file_name)}')">动作...</button>`;

          return `<tr>
            <td style="font-weight: 600; color: #fff; display: flex; align-items: center; white-space: nowrap;">
              ${fileIcon}<span title="${escapeHtml(fileLoc)}">${escapeHtml(fileLoc)}</span>
            </td>
            <td>
              <div style="font-family: Consolas, monospace; font-size: 11.5px; background: rgba(0,0,0,0.4); padding: 3px 8px; border-radius: 4px; color: #a8d1ff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 380px;">${lineSnippet}</div>
            </td>
            <td style="color: var(--text-secondary);">${h.score || 100}</td>
            <td style="color: var(--text-tertiary); font-family: monospace; font-size: 11px;" title="${escapeHtml(h.file_path)}">${escapeHtml(h.file_path)}</td>
            <td style="text-align: right; white-space: nowrap;">${actionsHtml}</td>
          </tr>`;
        }).join('');
      } else {
        tbody.innerHTML = currentSearchHits.map(h => {
          let qualityBadge = '<span class="badge-pill badge-neutral">模糊子序列</span>';
          if (h.match_quality === 'Exact') qualityBadge = '<span class="badge-pill badge-safe">精确匹配</span>';
          else if (h.match_quality === 'Prefix') qualityBadge = '<span class="badge-pill badge-safe">前缀匹配</span>';
          else if (h.match_quality === 'Suffix') qualityBadge = '<span class="badge-pill badge-neutral">后缀匹配</span>';
          else if (h.match_quality === 'TypoTolerant') qualityBadge = '<span class="badge-pill badge-warn" style="color:#ffb900; background:rgba(255,185,0,0.15);">1-edit 容错纠正</span>';

          const sizeStr = h.is_dir ? '<span style="color:var(--text-tertiary);">[目录]</span>' : formatBytes(h.size_bytes);
          const iconSvg = h.is_dir 
            ? '<svg style="width:14px;height:14px;fill:#ffb900;margin-right:6px;" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>'
            : '<svg style="width:14px;height:14px;fill:var(--text-secondary);margin-right:6px;" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>';

          let actionsHtml = `<button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapePath(h.path)}')">定位</button>`;
          actionsHtml += ` <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="triggerQuickSwitch('${escapePath(h.path)}')" title="跳转至当前前台文件选择对话框 (Listary 看家本领)">跳转</button>`;
          actionsHtml += ` <button class="btn btn-primary" style="padding: 2px 8px; font-size: 11px;" onclick="openActionRunnerModal('${escapePath(h.path)}', '${escapeHtml(h.name)}')" title="展开 Listary 动作流水线">动作...</button>`;
          if (h.can_check_lock) {
            actionsHtml += ` <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="checkFileLockQuick('${escapePath(h.path)}')">查锁</button>`;
          }
          if (h.can_junction_migrate) {
            actionsHtml += ` <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="startJunctionMigrateQuick('${escapePath(h.path)}')">搬迁</button>`;
          }

          return `<tr>
            <td style="font-weight: 600; color: #fff; display: flex; align-items: center;">${iconSvg}<span title="${escapeHtml(h.name)}">${escapeHtml(h.name)}</span></td>
            <td>${qualityBadge}</td>
            <td style="color: var(--text-secondary);">${sizeStr}</td>
            <td style="color: var(--text-tertiary); font-family: monospace; font-size: 11px;" title="${escapeHtml(h.path)}">${escapeHtml(h.path)}</td>
            <td style="text-align: right; white-space: nowrap;">${actionsHtml}</td>
          </tr>`;
        }).join('');
      }
    }

    async function executeDiskSearch(query) {
      const tbody = document.getElementById('searchResultsTableBody');
      const title = document.getElementById('searchResultsCountTitle');
      const latencyStats = document.getElementById('searchLatencyStats');
      const launcherContainer = document.getElementById('launcherHitContainer');
      if (!tbody) return;

      currentLauncherHit = null;
      if (launcherContainer) {
        launcherContainer.style.display = 'none';
        launcherContainer.innerHTML = '';
      }

      if (!query && mainSearchCurrentCategory === 'all') {
        currentSearchHits = [];
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 36px; color: var(--text-tertiary);">请输入检索词、拼音首字母(如jsq/wx)或点击分类药丸/预设，体验 ~1ms 极速检索与治理动作</td></tr>';
        if (title) title.innerText = '检索结果 (0 项)';
        return;
      }

      const isGrepMode = query.startsWith('grep:') || query.startsWith('sym:') || currentSearchSubMode === 'grep';
      currentSearchGrepMode = isGrepMode;
      updateSearchSortHeaders();

      let effectiveQuery = query;
      if (!isGrepMode && !devNoiseShieldEnabled && !query.includes('shield:')) {
        effectiveQuery = query + ' shield:0';
      }

      const t0 = performance.now();
      try {
        let endpoint = isGrepMode 
          ? ('/api/search/grep?q=' + encodeURIComponent(effectiveQuery))
          : ('/api/search/query?q=' + encodeURIComponent(effectiveQuery));

        if (!isGrepMode && mainSearchCurrentCategory && mainSearchCurrentCategory !== 'all') {
          endpoint += (endpoint.includes('?') ? '&' : '?') + 'category=' + encodeURIComponent(mainSearchCurrentCategory);
        }

        const res = await fetch(endpoint);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        const elapsedMs = (performance.now() - t0).toFixed(2);
        
        if (latencyStats) {
          latencyStats.innerHTML = `<span>本次检索耗时: <strong>${elapsedMs} ms</strong> (命中了 ${data.total_hits} 项)</span>`;
        }
        if (title) title.innerText = `检索结果 (${data.total_hits} 项)`;

        // 渲染 Pro Launcher 直达动作条目
        if (data.launcher_hit && launcherContainer) {
          currentLauncherHit = data.launcher_hit;
          launcherContainer.style.display = 'block';
          launcherContainer.innerHTML = `
            <div style="background: linear-gradient(135deg, rgba(96, 205, 255, 0.12), rgba(0, 120, 212, 0.08)); border: 1.5px solid rgba(96, 205, 255, 0.4); border-radius: var(--radius-md); padding: 12px 18px; display: flex; align-items: center; justify-content: space-between; gap: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.25);">
              <div style="display: flex; align-items: center; gap: 12px; overflow: hidden;">
                <div style="background: #60cdff; color: #080b10; font-weight: 700; font-size: 11px; padding: 4px 8px; border-radius: 4px; white-space: nowrap;">PRO 直达</div>
                <div style="overflow: hidden;">
                  <div style="font-weight: 700; font-size: 13.5px; color: #fff;">${escapeHtml(data.launcher_hit.title)}</div>
                  <div style="font-size: 11.5px; color: var(--text-secondary); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(data.launcher_hit.description)}</div>
                </div>
              </div>
              <button class="btn btn-primary" style="white-space: nowrap; font-weight: 600;" onclick="executeLauncherAction('${escapeHtml(data.launcher_hit.action_type)}', '${escapePath(data.launcher_hit.target)}')">
                执行 (${escapeHtml(data.launcher_hit.shortcut_label || 'Enter')})
              </button>
            </div>
          `;
        }

        currentSearchHits = data.hits || [];
        if (currentSearchHits.length === 0 && !data.launcher_hit) {
          tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 36px; color: var(--text-tertiary);">未找到与 "' + escapeHtml(query) + '" 匹配的' + (isGrepMode ? '代码行或符号' : '文件或目录') + '</td></tr>';
          return;
        }

        if (currentSearchSort.col) {
          sortAndRenderSearchResults();
        } else {
          renderSearchResultsTableRows();
        }

      } catch(e) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 24px; color: var(--status-danger);">检索失败: ' + escapeHtml(e.message) + '</td></tr>';
      }
    }

    function checkFileLockQuick(path) {
      revealInExplorer(path);
      checkCommonProcessLocks();
    }

    function startJunctionMigrateQuick(path) {
      switchTab('tools');
      setTimeout(() => {
        const inp = document.getElementById('migrateSourcePath');
        if (inp) {
          inp.value = path;
          inp.focus();
        }
      }, 100);
    }

    function setAnalyzeSubView(mode, el) {
      document.querySelectorAll('#analyzeFilterTabs .filter-tab').forEach(t => t.classList.remove('active'));
      if (el) el.classList.add('active');
      if (mode === 'giant') {
        document.getElementById('subviewGiantFiles').style.display = 'flex';
        document.getElementById('subviewDuplicates').style.display = 'none';
        if (state.giantFiles.length === 0) loadGiantFiles();
      } else {
        document.getElementById('subviewGiantFiles').style.display = 'none';
        document.getElementById('subviewDuplicates').style.display = 'flex';
      }
    }

    function setPurgeSubView(mode, el) {
      document.querySelectorAll('#purgeFilterTabs .filter-tab').forEach(t => t.classList.remove('active'));
      if (el) el.classList.add('active');
      if (mode === 'leftovers') {
        document.getElementById('subviewLeftovers').style.display = 'flex';
        document.getElementById('subviewRegistry').style.display = 'none';
        if (state.appLeftovers.length === 0) loadAppLeftovers();
      } else {
        document.getElementById('subviewLeftovers').style.display = 'none';
        document.getElementById('subviewRegistry').style.display = 'flex';
        if (state.registryIssues.length === 0) loadRegistryIssues();
      }
    }

    // Inspector Control
    function toggleInspector(open) {
      const el = document.getElementById('desktopInspector');
      if (open) el.classList.remove('collapsed');
      else el.classList.add('collapsed');
    }

    function openInspectorByCategory(catId) {
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === catId);
      if (cat) {
        inspectItem({
          name: cat.name,
          category: '空间分类',
          path: cat.rules.map(r => r.path_pattern).join('; '),
          size_bytes: cat.total_size_bytes,
          file_count: cat.total_files
        });
      }
    }

    function inspectItem(item) {
      state.inspectorTarget = item;
      document.getElementById('inspName').innerText = item.name || item.path.split('\\').pop() || '未命名资产';
      document.getElementById('inspCategory').innerText = item.category || '通用缓存';
      document.getElementById('inspPath').innerText = item.path;
      document.getElementById('inspSize').innerText = formatBytes(item.size_bytes || 0);
      document.getElementById('inspFiles').innerText = item.file_count ? `${item.file_count} 个文件` : '单个文件';

      const lockEl = document.getElementById('inspLockStatus');
      lockEl.innerText = '正在检测进程占用...';
      lockEl.style.color = 'var(--text-tertiary)';

      fetch('/api/check-path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: item.path })
      })
      .then(res => res.json())
      .then(data => {
        if (data.locking_processes && data.locking_processes.length > 0) {
          lockEl.innerText = `警告: 被进程 [${data.locking_processes.join(', ')}] 独占锁定`;
          lockEl.style.color = 'var(--status-warn)';
        } else {
          lockEl.innerText = '进程未锁定 · 100% 安全可处理';
          lockEl.style.color = 'var(--status-safe)';
        }
      })
      .catch(() => {
        lockEl.innerText = '常规未加锁状态';
        lockEl.style.color = 'var(--status-safe)';
      });

      toggleInspector(true);
    }

    function copyInspectorPath() {
      if (state.inspectorTarget && state.inspectorTarget.path) {
        navigator.clipboard.writeText(state.inspectorTarget.path);
        showToast('已复制绝对路径到剪贴板');
      }
    }

    function revealCurrentInspectorPath() {
      if (state.inspectorTarget && state.inspectorTarget.path) {
        revealInExplorer(state.inspectorTarget.path);
      }
    }

    function cleanCurrentInspectorItem() {
      if (state.inspectorTarget && state.inspectorTarget.path) {
        deleteSingleItem(state.inspectorTarget.path);
      }
    }

    // Context Menu
    window.addEventListener('contextmenu', (e) => {
      const row = e.target.closest('tr[data-path]');
      if (!row) {
        closeContextMenu();
        return;
      }
      e.preventDefault();
      const p = row.getAttribute('data-path');
      const name = row.getAttribute('data-name') || p.split('\\').pop();
      const size = parseInt(row.getAttribute('data-size') || '0', 10);
      const cat = row.getAttribute('data-cat') || '普通资产';

      state.contextTarget = { path: p, name, size_bytes: size, category: cat };

      const menu = document.getElementById('desktopContextMenu');
      menu.style.left = `${Math.min(e.clientX, window.innerWidth - 210)}px`;
      menu.style.top = `${Math.min(e.clientY, window.innerHeight - 170)}px`;
      menu.classList.add('active');
    });

    window.addEventListener('click', () => { closeContextMenu(); });
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeContextMenu();
        closeConfirmModal();
        toggleInspector(false);
      } else if (e.key === 'F5' || (e.ctrlKey && e.key.toLowerCase() === 'r')) {
        e.preventDefault();
        runScan();
      } else if (e.ctrlKey && e.key.toLowerCase() === 'f') {
        e.preventDefault();
        switchTab('search');
      }
    });

    function closeContextMenu() {
      document.getElementById('desktopContextMenu').classList.remove('active');
    }
    function onContextReveal() {
      if (state.contextTarget) revealInExplorer(state.contextTarget.path);
      closeContextMenu();
    }
    function onContextInspect() {
      if (state.contextTarget) inspectItem(state.contextTarget);
      closeContextMenu();
    }
    function onContextCopyPath() {
      if (state.contextTarget) {
        navigator.clipboard.writeText(state.contextTarget.path);
        showToast('已复制路径');
      }
      closeContextMenu();
    }
    function onContextClean() {
      if (state.contextTarget) deleteSingleItem(state.contextTarget.path);
      closeContextMenu();
    }

    // Disk Management
    async function refreshDisks() {
      try {
        const res = await fetch('/api/disks');
        state.disks = await res.json();
        renderDiskSelector();
      } catch (e) {
        console.error('Failed to fetch disks', e);
      }
    }

    function renderDiskSelector() {
      const c = document.getElementById('diskSelectorContainer');
      c.innerHTML = '';
      state.disks.forEach(d => {
        const freeGb = (d.free_bytes / (1024**3)).toFixed(1);
        const totalGb = (d.total_bytes / (1024**3)).toFixed(0);
        const isActive = d.letter === state.currentDrive;

        const pill = document.createElement('div');
        pill.className = `drive-pill ${isActive ? 'active' : ''}`;
        pill.innerHTML = `<span class="drive-pill-dot" style="background:${d.usage_percent > 85 ? 'var(--status-warn)' : 'var(--status-safe)'}"></span><span>${d.letter} (${freeGb} GB 可用 / ${totalGb} GB)</span>`;
        pill.onclick = () => {
          state.currentDrive = d.letter;
          renderDiskSelector();
          showToast(`已切换至 ${d.letter} 盘视图`);
        };
        c.appendChild(pill);

        if (isActive) {
          document.getElementById('sbDriveLetter').innerText = d.letter;
          document.getElementById('sbDriveFree').innerText = `${freeGb} GB`;
          document.getElementById('sbDiskDetails').innerText = `${d.letter} 盘 ${freeGb} GB 可用 / ${totalGb} GB (${d.usage_percent}%)`;
        }
      });
    }

    // Full Scan
    async function runScan() {
      showToast('正在执行全盘空间健康体检...');
      document.getElementById('sbProgress').innerText = '正在扫描...';

      try {
        const res = await fetch('/api/scan');
        state.scanReport = await res.json();
        state.selectedPaths.clear();

        let totalReclaimable = 0;
        state.scanReport.categories.forEach(cat => {
          cat.rules.forEach(rule => {
            rule.matched_paths.forEach(mp => {
              if (mp.size_bytes > 0) {
                totalReclaimable += mp.size_bytes;
                if (rule.default_checked) {
                  state.selectedPaths.add(mp.path);
                }
              }
            });
          });
        });

        const totalGbStr = (totalReclaimable / (1024**3)).toFixed(1);
        if (document.getElementById('heroReclaimNum')) document.getElementById('heroReclaimNum').innerText = totalGbStr;
        if (document.getElementById('badgeClean')) document.getElementById('badgeClean').innerText = `${totalGbStr} GB`;
        if (document.getElementById('heroBtnCleanText')) document.getElementById('heroBtnCleanText').innerText = `一键快速清理 (${totalGbStr} GB)`;

        // Update Gauge Circle stroke-dashoffset
        const circle = document.getElementById('heroGaugeCircle');
        if (circle) {
          const offset = Math.max(80, 440 - Math.min(360, (totalReclaimable / (40 * 1024**3)) * 360));
          circle.style.strokeDashoffset = offset;
        }

        // Update Card Metrics
        const sysCat = state.scanReport.categories.find(c => c.id === 'system');
        if (sysCat && document.getElementById('cardSystemMetric')) document.getElementById('cardSystemMetric').innerHTML = formatMetricHtml(sysCat.total_size_bytes);

        const devCat = state.scanReport.categories.find(c => c.id === 'dev_cache');
        if (devCat) {
          if (document.getElementById('cardDevMetric')) document.getElementById('cardDevMetric').innerHTML = formatMetricHtml(devCat.total_size_bytes);
          if (document.getElementById('badgeDevCache')) document.getElementById('badgeDevCache').innerText = formatBytes(devCat.total_size_bytes);
        }

        const offCat = state.scanReport.categories.find(c => c.id === 'office_chat');
        if (offCat) {
          if (document.getElementById('cardOfficeMetric')) document.getElementById('cardOfficeMetric').innerHTML = formatMetricHtml(offCat.total_size_bytes);
          if (document.getElementById('badgeOffice')) document.getElementById('badgeOffice').innerText = formatBytes(offCat.total_size_bytes);
        }

        const docCat = state.scanReport.categories.find(c => c.id === 'docker_virtual');
        if (docCat) {
          if (document.getElementById('cardDockerMetric')) document.getElementById('cardDockerMetric').innerHTML = formatMetricHtml(docCat.total_size_bytes);
          if (document.getElementById('badgeDocker')) document.getElementById('badgeDocker').innerText = formatBytes(docCat.total_size_bytes);
        }

        const bCat = state.scanReport.categories.find(c => c.id === 'browser_cache');
        if (bCat) {
          if (document.getElementById('cardBrowserMetric')) document.getElementById('cardBrowserMetric').innerHTML = formatMetricHtml(bCat.total_size_bytes);
          if (document.getElementById('badgeBrowser')) document.getElementById('badgeBrowser').innerText = formatBytes(bCat.total_size_bytes);
        }

        const vacCat = state.scanReport.categories.find(c => c.id === 'sqlite_optimize' || c.id === 'db_vacuum');
        if (vacCat && document.getElementById('cardVacuumMetric')) document.getElementById('cardVacuumMetric').innerHTML = formatMetricHtml(vacCat.total_size_bytes);

        state.selectedPaths.clear();
        state.scanReport.categories.forEach(cat => {
          cat.rules.forEach(rule => {
            rule.matched_paths.forEach(mp => {
              if (mp.size_bytes > 0) state.selectedPaths.add(mp.path);
            });
          });
        });

        updateSpectrumDistribution(state.scanReport, totalReclaimable);

        renderOverviewTable();
        renderDevCacheTable();
        renderOfficeTable();
        renderDockerTable();
        renderBrowserTable();
        renderVacuumTable();
        renderCustomRulesTable();

        const sbProg = document.getElementById('sbProgress');
        if (sbProg) sbProg.innerText = '体检完成';
        updateSelectionStatus();
        showToast('空间体检完成，已识别可释放空间');
      } catch (e) {
        console.error('Scan error', e);
        showToast('体检失败: ' + e.message);
      }
    }

    function renderOverviewTable() {
      const tbody = document.getElementById('overviewTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      if (!state.scanReport) return;

      const q = (document.getElementById('overviewSearchInput')?.value || '').toLowerCase();
      let renderedCount = 0;

      state.scanReport.categories.forEach(cat => {
        cat.rules.forEach(rule => {
          rule.matched_paths.forEach(mp => {
            if (mp.size_bytes === 0) return;
            if (q && !rule.name.toLowerCase().includes(q) && !mp.path.toLowerCase().includes(q)) return;

            renderedCount++;
            const tr = document.createElement('tr');
            tr.setAttribute('data-path', mp.path);
            tr.setAttribute('data-name', rule.name);
            tr.setAttribute('data-size', mp.size_bytes);
            tr.setAttribute('data-cat', cat.name);

            const isChecked = state.selectedPaths.has(mp.path);
            tr.onclick = (e) => {
              if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
                document.querySelectorAll('.data-grid tbody tr').forEach(r => r.classList.remove('selected'));
                tr.classList.add('selected');
                inspectItem({ name: rule.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: cat.name });
              }
            };

            tr.innerHTML = `
              <td class="col-checkbox">
                <input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleItemSelect('${escapeHtml(mp.path)}', this.checked)">
              </td>
              <td style="font-weight:600;">${escapeHtml(rule.name)}</td>
              <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
              <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
              <td style="text-align: right; color: var(--text-tertiary);">${mp.file_count}</td>
              <td style="text-align: center;">
                <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(mp.path)}')">定位</button>
              </td>
            `;
            tbody.appendChild(tr);
          });
        });
      });

      const oc = document.getElementById('overviewCounter');
      if (oc) oc.innerText = `已检出 ${renderedCount} 处清理项`;
    }

    function toggleItemSelect(path, checked) {
      if (checked) state.selectedPaths.add(path);
      else state.selectedPaths.delete(path);
      updateSelectionStatus();
    }

    function toggleSelectAllOverview(checked) {
      state.selectedPaths.clear();
      if (checked && state.scanReport) {
        state.scanReport.categories.forEach(cat => {
          cat.rules.forEach(rule => {
            rule.matched_paths.forEach(mp => {
              if (mp.size_bytes > 0) state.selectedPaths.add(mp.path);
            });
          });
        });
      }
      renderOverviewTable();
      updateSelectionStatus();
    }

    function setOverviewFilter(filter, el) {
      document.querySelectorAll('#pane-overview .filter-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderOverviewTable();
    }

    function filterOverviewTable() {
      renderOverviewTable();
    }

    function updateSelectionStatus() {
      let selBytes = 0;
      if (state.scanReport) {
        state.scanReport.categories.forEach(cat => {
          cat.rules.forEach(rule => {
            rule.matched_paths.forEach(mp => {
              if (state.selectedPaths.has(mp.path)) {
                selBytes += mp.size_bytes;
              }
            });
          });
        });
      }
      const sbSel = document.getElementById('sbSelection');
      if (sbSel) sbSel.innerText = `已选 ${state.selectedPaths.size} 项 (${formatBytes(selBytes)})`;
      const btnClean = document.getElementById('heroBtnCleanText');
      if (btnClean) btnClean.innerText = `一键快速清理 (${formatBytes(selBytes)})`;
    }

    // Render Office & WeChat Table
    function renderOfficeTable() {
      const tbody = document.getElementById("officeTableBody");
      if (!tbody) return;
      tbody.innerHTML = "";
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === "office_chat");
      if (!cat) return;

      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          if (mp.size_bytes === 0) return;
          const tr = document.createElement("tr");
          tr.setAttribute("data-path", mp.path);
          tr.setAttribute("data-name", r.name);
          tr.setAttribute("data-size", mp.size_bytes);
          tr.setAttribute("data-cat", "办公与社交");
          tr.onclick = (e) => {
            if (e.target.tagName !== "INPUT" && e.target.tagName !== "BUTTON") {
              document.querySelectorAll(".data-grid tbody tr").forEach(row => row.classList.remove("selected"));
              tr.classList.add("selected");
              inspectItem(mp.path, r.name, mp.size_bytes, mp.file_count, "办公与社交");
            }
          };

          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked onchange="updateSelectionStatus()"></td>
            <td><span style="font-weight:600; color:#fff;">${escapeHtml(r.name)}</span></td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align:right; font-family:var(--font-mono); font-weight:600; color:#60cdff;">${formatBytes(mp.size_bytes)}</td>
            <td style="text-align:right; font-family:var(--font-mono); color:var(--text-tertiary);">${mp.file_count}</td>
            <td style="text-align:center;">
              <button class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="event.stopPropagation(); revealPath('${escapeHtml(mp.path).replace(/\\/g, "\\\\")}')">定位</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    // Render Docker Virtual Table
    function renderDockerTable() {
      const tbody = document.getElementById("dockerTableBody");
      if (!tbody) return;
      tbody.innerHTML = "";
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === "docker_virtual");
      if (!cat) return;

      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          if (mp.size_bytes === 0) return;
          const tr = document.createElement("tr");
          tr.setAttribute("data-path", mp.path);
          tr.setAttribute("data-name", r.name);
          tr.setAttribute("data-size", mp.size_bytes);
          tr.setAttribute("data-cat", "Docker虚拟");
          tr.onclick = (e) => {
            if (e.target.tagName !== "INPUT" && e.target.tagName !== "BUTTON") {
              document.querySelectorAll(".data-grid tbody tr").forEach(row => row.classList.remove("selected"));
              tr.classList.add("selected");
              inspectItem(mp.path, r.name, mp.size_bytes, mp.file_count, "Docker虚拟");
            }
          };

          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked onchange="updateSelectionStatus()"></td>
            <td><span style="font-weight:600; color:#fff;">${escapeHtml(r.name)}</span></td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align:right; font-family:var(--font-mono); font-weight:600; color:#60cdff;">${formatBytes(mp.size_bytes)}</td>
            <td style="text-align:right; font-family:var(--font-mono); color:var(--text-tertiary);">${mp.file_count}</td>
            <td style="text-align:center;">
              <button class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="event.stopPropagation(); revealPath('${escapeHtml(mp.path).replace(/\\/g, "\\\\")}')">定位</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    // Load Docker Engine live status
    async function loadDockerStatus() {
      try {
        const res = await fetch("/api/docker/status");
        const data = await res.json();
        if (data && data.available && data.running && data.items) {
          const imgItem = data.items.find(i => i.item_type === "Images");
          if (imgItem) {
            document.getElementById("dockerImagesMetric").innerHTML = `<span class="metric-num">${imgItem.total_size.replace("GB","")}</span><span class="metric-unit">GB</span>`;
            document.getElementById("dockerImagesDesc").innerText = `${imgItem.total_count} 个镜像 · ${imgItem.reclaimable} 可回收`;
          }
          const bldItem = data.items.find(i => i.item_type === "Build Cache");
          if (bldItem) {
            document.getElementById("dockerBuilderMetric").innerHTML = `<span class="metric-num">${bldItem.total_size.replace("GB","")}</span><span class="metric-unit">GB</span>`;
          }
          const volItem = data.items.find(i => i.item_type === "Local Volumes");
          if (volItem) {
            document.getElementById("dockerVolumesMetric").innerHTML = `<span class="metric-num">${volItem.total_size.replace("GB","")}</span><span class="metric-unit">GB</span>`;
            document.getElementById("dockerVolumesDesc").innerText = `${volItem.total_count} 个本地卷 · ${volItem.reclaimable} 未挂载`;
          }
        }
      } catch (err) {
        console.warn("Docker status fetch error:", err);
      }
    }

    // Execute Docker prune
    async function pruneDocker(target) {
      const targetLabels = {
        "builder": "Docker 构建缓存",
        "images": "虚悬无用容器镜像",
        "all": "Docker 全量未激活容器与镜像"
      };
      const label = targetLabels[target] || target;
      if (!confirm(`确定执行清理: ${label} 吗？`)) return;

      showToast(`正在执行 ${label} 清理...`);
      try {
        const res = await fetch("/api/docker/prune", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ target })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`${label} 清理完成！`);
          loadDockerStatus();
          runScan();
        } else {
          showToast(`清理失败: ${data.error || "未知错误"}`);
        }
      } catch (err) {
        showToast("请求失败: " + err.message);
      }
    }

    state.devFilter = 'all';

    function setDevFilter(filter, el) {
      state.devFilter = filter;
      document.querySelectorAll('#devFilterTabs .filter-tab').forEach(t => t.classList.remove('active'));
      if (el) el.classList.add('active');
      renderDevCacheTable();
    }

    function toggleSelectAllCategory(catId, masterCheckbox) {
      const checked = masterCheckbox.checked;
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === catId);
      if (!cat) return;
      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          if (mp.size_bytes > 0) {
            if (checked) state.selectedPaths.add(mp.path);
            else state.selectedPaths.delete(mp.path);
          }
        });
      });
      if (catId === 'dev_cache') renderDevCacheTable();
      if (catId === 'office_chat') renderOfficeTable();
      if (catId === 'docker_virtual') renderDockerTable();
      if (catId === 'browser_cache') renderBrowserTable();
      renderOverviewTable();
      updateSelectionStatus();
    }

    // Dev Cache & Design Studio Table
    function renderDevCacheTable() {
      const tbody = document.getElementById('devCacheTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === 'dev_cache');
      if (!cat) return;

      const filter = state.devFilter || 'all';
      let matchCount = 0;

      const tagBadgeMap = {
        'ide': '<span class="tag-pill tag-blue">IDE</span>',
        'pkg': '<span class="tag-pill tag-green">包管理</span>',
        'creative': '<span class="tag-pill tag-purple">Adobe</span>',
        'runtime': '<span class="tag-pill tag-orange">运行时</span>'
      };

      cat.rules.forEach(r => {
        if (filter !== 'all' && r.tag !== filter) return;
        r.matched_paths.forEach(mp => {
          if (mp.size_bytes === 0) return;
          matchCount++;
          const tr = document.createElement('tr');
          tr.setAttribute('data-path', mp.path);
          tr.setAttribute('data-name', r.name);
          tr.setAttribute('data-size', mp.size_bytes);
          tr.setAttribute('data-cat', '开发与设计');
          tr.onclick = (e) => {
            if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
              document.querySelectorAll('.data-grid tbody tr').forEach(row => row.classList.remove('selected'));
              tr.classList.add('selected');
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: '开发与设计' });
            }
          };

          const isChecked = state.selectedPaths.has(mp.path);
          const badge = tagBadgeMap[r.tag] || '<span class="tag-pill tag-blue">DEV</span>';

          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleItemSelect('${escapeHtml(mp.path)}', this.checked)"></td>
            <td>${badge}<span style="font-weight:600; color:#fff;">${escapeHtml(r.name)}</span></td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #60cdff;">${formatBytes(mp.size_bytes)}</td>
            <td style="text-align: right; font-family: var(--font-mono); color: var(--text-tertiary);">${mp.file_count}</td>
            <td style="text-align: center;">
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="event.stopPropagation(); revealInExplorer('${escapeHtml(mp.path)}')">定位</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });

      const summaryEl = document.getElementById('devSummaryCount');
      if (summaryEl) summaryEl.innerText = `显示 ${matchCount} 个专清目标`;
    }

    // Browser Cache Table
    function renderBrowserTable() {
      const tbody = document.getElementById('browserTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === 'browser_cache');
      if (!cat) return;

      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          if (mp.size_bytes === 0) return;
          const tr = document.createElement('tr');
          tr.setAttribute('data-path', mp.path);
          tr.setAttribute('data-name', r.name);
          tr.setAttribute('data-size', mp.size_bytes);
          tr.setAttribute('data-cat', '浏览器缓存');
          tr.onclick = (e) => {
            if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
              document.querySelectorAll('.data-grid tbody tr').forEach(row => row.classList.remove('selected'));
              tr.classList.add('selected');
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: '浏览器缓存' });
            }
          };
          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked></td>
            <td style="font-weight:600;">${escapeHtml(r.name)}</td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
            <td style="text-align: right; color: var(--text-tertiary);">${mp.file_count}</td>
            <td style="text-align: center;">
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(mp.path)}')">定位</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    // Vacuum Table
    function renderVacuumTable() {
      const tbody = document.getElementById('vacuumTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === 'sqlite_optimize' || c.id === 'db_vacuum');
      if (!cat) return;

      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          const tr = document.createElement('tr');
          tr.setAttribute('data-path', mp.path);
          tr.setAttribute('data-name', r.name);
          tr.setAttribute('data-size', mp.size_bytes);
          tr.setAttribute('data-cat', 'SQLite 数据库');
          tr.onclick = (e) => {
            if (e.target.tagName !== 'BUTTON') {
              document.querySelectorAll('.data-grid tbody tr').forEach(row => row.classList.remove('selected'));
              tr.classList.add('selected');
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: 'SQLite 数据库' });
            }
          };
          tr.innerHTML = `
            <td style="font-weight:600;">${escapeHtml(r.name)}</td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
            <td style="text-align: center;"><span class="badge-pill badge-safe">无损压缩碎片</span></td>
            <td style="text-align: center;">
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="vacuumDatabase('${escapeHtml(mp.path)}')">执行 VACUUM</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    // Registry Scanner
    async function loadRegistryIssues() {
      showToast('正在深度排查无效卸载信息与死链注册表项...');
      const regCounter = document.getElementById('registryCounter');
      if (regCounter) regCounter.innerText = '扫描中...';
      try {
        const res = await fetch('/api/registry/scan');
        state.registryIssues = await res.json();
        state.selectedRegistryIds = new Set(state.registryIssues.map(i => i.id));
        if (document.getElementById('badgeRegistry')) document.getElementById('badgeRegistry').innerText = state.registryIssues.length;
        if (document.getElementById('badgePurge')) document.getElementById('badgePurge').innerText = `${state.registryIssues.length + state.appLeftovers.length} 处`;
        renderRegistryTable();
        showToast(`排查出 ${state.registryIssues.length} 处失效注册表条目`);
      } catch (e) {
        showToast('注册表扫描失败: ' + e.message);
      }
    }

    function renderRegistryTable() {
      const tbody = document.getElementById('registryTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      const q = (document.getElementById('registrySearchInput')?.value || '').toLowerCase();
      const filtered = state.registryIssues.filter(item => {
        if (state.registryFilterCategory === 'mui' && !item.category.includes('MUICache')) return false;
        if (state.registryFilterCategory === 'openwith' && !item.category.includes('OpenWith')) return false;
        if (state.registryFilterCategory === 'uninst' && !item.category.includes('Uninstall')) return false;
        if (q) return item.invalid_path.toLowerCase().includes(q) || item.category.toLowerCase().includes(q) || item.root_key.toLowerCase().includes(q);
        return true;
      });

      const rc = document.getElementById('registryCounter');
      if (rc) rc.innerText = `发现 ${filtered.length} 处冗余项目`;
      const btnClean = document.getElementById('btnCleanRegistryLabel');
      if (btnClean) btnClean.innerText = `一键安全修复 (${state.selectedRegistryIds.size} 项)`;

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 30px; color: var(--text-tertiary);">当前注册表环境干净，未发现死链残留</td></tr>`;
        return;
      }

      filtered.forEach(item => {
        const tr = document.createElement('tr');
        const isChecked = state.selectedRegistryIds.has(item.id);
        tr.onclick = (e) => {
          if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
            inspectItem({ name: item.category, path: item.invalid_path, size_bytes: 0, category: item.root_key });
          }
        };

        const badgeClass = item.category.includes('OpenWith') ? 'badge-openwith' : item.category.includes('MUICache') ? 'badge-warn' : 'badge-danger';
        tr.innerHTML = `
          <td class="col-checkbox"><input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleRegistryItem('${item.id}', this.checked)"></td>
          <td><span class="badge-pill ${badgeClass}">${escapeHtml(item.category)}</span></td>
          <td><span class="path-text" title="${escapeHtml(item.invalid_path)}" style="color:#ff99a4;">${escapeHtml(item.invalid_path)}</span></td>
          <td><span class="path-text" title="${escapeHtml(item.root_key)}">${escapeHtml(item.root_key)}</span></td>
          <td><span class="badge-pill badge-safe">安全可修复</span></td>
          <td style="text-align: center;">
            <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="cleanSingleRegistryItem('${item.id}')">修复</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function toggleRegistryItem(id, checked) {
      if (checked) state.selectedRegistryIds.add(id);
      else state.selectedRegistryIds.delete(id);
      document.getElementById('btnCleanRegistryLabel').innerText = `一键安全修复 (${state.selectedRegistryIds.size} 项)`;
    }

    function toggleSelectAllRegistry(checked) {
      state.selectedRegistryIds.clear();
      if (checked) state.registryIssues.forEach(i => state.selectedRegistryIds.add(i.id));
      renderRegistryTable();
    }

    function setRegistryFilter(cat, el) {
      state.registryFilterCategory = cat;
      document.querySelectorAll('#pane-registry .filter-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderRegistryTable();
    }

    function executeCleanRegistry() {
      if (state.selectedRegistryIds.size === 0) {
        showToast('请至少选择一项需要修复的注册表项目');
        return;
      }
      openConfirmModal('注册表修复确认', `即将安全清理 ${state.selectedRegistryIds.size} 项死链注册表值。<br><br>系统将在临时目录下自动生成带有时间戳的 .reg 回滚备份文件。`, async () => {
        closeConfirmModal();
        showToast('正在导出 .reg 备份并修复注册表...');
        try {
          const res = await fetch('/api/registry/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ids: Array.from(state.selectedRegistryIds) })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`修复完成！已处理 ${data.deleted_count} 项，备份保存在: ${data.backup_file}`);
            loadRegistryIssues();
          } else {
            showToast('部分注册表项清理失败: ' + (data.errors ? data.errors.join(', ') : ''));
          }
        } catch (e) {
          showToast('修复注册表请求失败: ' + e.message);
        }
      });
    }

    // Giant Files Scanner
    async function loadGiantFiles() {
      showToast('正在多线程全盘检索 100MB+ 沉淀文件...');
      const gc = document.getElementById('giantCounter');
      if (gc) gc.innerText = '排查中...';
      const canvas = document.getElementById('giantTreemapCanvas');
      if (canvas && (!state.giantFiles || state.giantFiles.length === 0)) {
        canvas.innerHTML = '<div style="grid-column: span 12; grid-row: span 6; display: flex; align-items: center; justify-content: center; color: var(--text-tertiary); font-size: 13px; gap: 8px;"><span class="status-dot-pulse" style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span><span>正在全盘扫描 100MB+ 巨型资产并构建 Treemap 空间树图...</span></div>';
      }
      try {
        const res = await fetch('/api/giant-files');
        state.giantFiles = await res.json();
        if (document.getElementById('badgeGiantFiles')) document.getElementById('badgeGiantFiles').innerText = state.giantFiles.length;
        if (document.getElementById('badgeAnalyze')) document.getElementById('badgeAnalyze').innerText = `${state.giantFiles.length} 项`;
        if (document.getElementById('cardGiantMetric')) document.getElementById('cardGiantMetric').innerText = `${(state.giantFiles.reduce((acc, f) => acc + f.size_bytes, 0) / (1024**3)).toFixed(1)} GB`;
        renderGiantDistribution();
        renderGiantTreemap(state.giantFiles);
        renderGiantTable();
      } catch (e) {
        showToast('排查大文件失败: ' + e.message);
      }
    }

    function renderGiantDistribution() {
      const typeMap = {
        '数据库': { color: '#00bcf2', bytes: 0, count: 0, rawKeys: ['Database', '数据库'] },
        '虚拟机': { color: '#a855f7', bytes: 0, count: 0, rawKeys: ['VirtualDisk', '虚拟机'] },
        '安装包': { color: '#f59e0b', bytes: 0, count: 0, rawKeys: ['Installer', '安装包'] },
        '压缩包': { color: '#0078d4', bytes: 0, count: 0, rawKeys: ['Archive', '压缩包'] },
        '其它大资产': { color: '#64748b', bytes: 0, count: 0, rawKeys: ['Other', '其它大资产'] }
      };

      let totalBytes = 0;
      state.giantFiles.forEach(f => {
        totalBytes += f.size_bytes;
        let matched = false;
        for (const [k, meta] of Object.entries(typeMap)) {
          if (meta.rawKeys.includes(f.category)) {
            meta.bytes += f.size_bytes;
            meta.count += 1;
            matched = true;
            break;
          }
        }
        if (!matched) {
          typeMap['其它大资产'].bytes += f.size_bytes;
          typeMap['其它大资产'].count += 1;
        }
      });

      const giantSub = document.getElementById('giantTotalSubtitle');
      if (giantSub) giantSub.innerText = `总计 ${formatBytes(totalBytes)} (${state.giantFiles.length} 个文件)`;

      const bar = document.getElementById('giantDistributionBar');
      if (!bar) return;
      bar.innerHTML = '';
      const legend = document.getElementById('giantLegendList');
      if (!legend) return;
      legend.innerHTML = '';

      const allPill = document.createElement('div');
      allPill.style.cursor = 'pointer';
      allPill.className = 'filter-tab active';
      allPill.innerHTML = `<strong>全部资产 (${state.giantFiles.length})</strong>`;
      allPill.onclick = () => {
        currentGiantCategoryKeys = null;
        document.querySelectorAll('#giantLegendList .filter-tab').forEach(el => el.classList.remove('active'));
        allPill.classList.add('active');
        renderGiantTable();
      };
      legend.appendChild(allPill);

      for (const [name, meta] of Object.entries(typeMap)) {
        if (meta.bytes === 0) continue;
        const pct = ((meta.bytes / (totalBytes || 1)) * 100).toFixed(1);

        const seg = document.createElement('div');
        seg.style.width = `${pct}%`;
        seg.style.backgroundColor = meta.color;
        seg.style.height = '100%';
        seg.title = `${name}: ${formatBytes(meta.bytes)} (${pct}%)`;
        bar.appendChild(seg);

        const leg = document.createElement('div');
        leg.className = 'filter-tab';
        leg.style.display = 'flex';
        leg.style.alignItems = 'center';
        leg.style.gap = '6px';
        leg.style.cursor = 'pointer';
        leg.innerHTML = `<span style="width:8px; height:8px; border-radius:50%; background:${meta.color};"></span><span>${name} (${formatBytes(meta.bytes)})</span>`;
        leg.onclick = () => {
          currentGiantCategoryKeys = meta.rawKeys;
          document.querySelectorAll('#giantLegendList .filter-tab').forEach(el => el.classList.remove('active'));
          leg.classList.add('active');
          renderGiantTable();
        };
        legend.appendChild(leg);
      }
    }

    let currentGiantCategoryKeys = null;

    function setGiantSizeFilter(f, el) {
      state.giantSizeFilter = f;
      document.querySelectorAll('#pane-giant .filter-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderGiantTable();
    }

    function filterGiantTable() {
      renderGiantTable();
    }

    function renderGiantTable() {
      const tbody = document.getElementById('giantFilesTableBody') || document.getElementById('giantTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const q = (document.getElementById('giantSearchInput')?.value || '').toLowerCase();
      const filtered = state.giantFiles.filter(f => {
        if (currentGiantCategoryKeys && !currentGiantCategoryKeys.includes(f.category)) return false;
        if (state.giantSizeFilter === 'huge' && f.size_bytes < 1024**3) return false;
        if (state.giantSizeFilter === 'large' && (f.size_bytes < 500*1024*1024 || f.size_bytes >= 1024**3)) return false;
        if (state.giantSizeFilter === 'med' && f.size_bytes >= 500*1024*1024) return false;
        if (q && !f.name.toLowerCase().includes(q) && !f.path.toLowerCase().includes(q)) return false;
        return true;
      });

      const gc = document.getElementById('giantCounter');
      if (gc) gc.innerText = `已排查出 ${filtered.length} 个大型资产`;
      const agc = document.getElementById('analyzeGiantCount');
      if (agc) agc.innerText = `${filtered.length}`;

      filtered.forEach(f => {
        const tr = document.createElement('tr');
        tr.setAttribute('data-path', f.path);
        tr.setAttribute('data-name', f.name);
        tr.setAttribute('data-size', f.size_bytes);
        tr.setAttribute('data-cat', f.category || '大文件');
        tr.onclick = (e) => {
          if (e.target.tagName !== 'BUTTON') {
            document.querySelectorAll('.data-grid tbody tr').forEach(r => r.classList.remove('selected'));
            tr.classList.add('selected');
            inspectItem({ name: f.name, path: f.path, size_bytes: f.size_bytes, category: f.category || '大文件' });
          }
        };

        const mtimeStr = f.modified_timestamp ? new Date(f.modified_timestamp * 1000).toLocaleDateString() : '-';

        tr.innerHTML = `
          <td style="font-weight:600;"><span class="path-text" title="${escapeHtml(f.name)}" style="color:#ffffff;">${escapeHtml(f.name)}</span></td>
          <td><span class="path-text" title="${escapeHtml(f.path)}">${escapeHtml(f.path)}</span></td>
          <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #60cdff;">${formatBytes(f.size_bytes)}</td>
          <td style="text-align: center; color: var(--text-tertiary); font-size: 11px;">${mtimeStr}</td>
          <td style="text-align: center;">
            <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(f.path)}')">定位</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // ==========================================
    // Scheme 1: Visualization Upgrade Functions
    // ==========================================
    function updateSpectrumDistribution(report, totalReclaimable) {
      const container = document.getElementById('spectrumSegmentsBar');
      const legendGrid = document.getElementById('spectrumLegendGrid');
      const totalText = document.getElementById('spectrumTotalText');
      const reclaimVal = document.getElementById('spectrumReclaimVal');
      if (!container || !legendGrid) return;

      container.innerHTML = '';
      legendGrid.innerHTML = '';

      if (!report || !report.categories || totalReclaimable === 0) {
        container.innerHTML = '<div style="width:100%; height:100%; background:rgba(255,255,255,0.06); display:flex; align-items:center; justify-content:center; font-size:11px; color:var(--text-tertiary);">完成扫描后呈现空间色彩分布</div>';
        if (totalText) totalText.innerText = '0 B';
        if (reclaimVal) reclaimVal.innerText = '0 B';
        return;
      }

      if (totalText) totalText.innerText = formatBytes(totalReclaimable);
      if (reclaimVal) reclaimVal.innerText = formatBytes(totalReclaimable);

      const colorMap = {
        'system': { name: '系统临时', color: '#3b82f6' },
        'dev_cache': { name: '现代开发', color: '#10b981' },
        'office_chat': { name: '微信办公', color: '#a855f7' },
        'browser_cache': { name: '浏览器冗余', color: '#f59e0b' },
        'sqlite_optimize': { name: '数据库压缩', color: '#06b6d4' },
        'db_vacuum': { name: '数据库压缩', color: '#06b6d4' },
        'docker_virtual': { name: 'Docker虚拟化', color: '#6366f1' },
        'other': { name: '其他残留', color: '#64748b' }
      };

      const validCats = report.categories.filter(c => c.total_size_bytes > 0);
      if (validCats.length === 0) {
        container.innerHTML = '<div style="width:100%; height:100%; background:rgba(34,197,94,0.15); color:#22c55e; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:600;">系统极其干净，无可清理残留</div>';
        return;
      }

      validCats.forEach(cat => {
        let displayName = colorMap[cat.id]?.name || cat.name || '其他数据';
        if (displayName.includes('Junction') || displayName.includes('搬家')) displayName = '跨盘迁移 (Junction)';
        const meta = colorMap[cat.id] || { name: displayName, color: '#64748b' };
        const pct = ((cat.total_size_bytes / totalReclaimable) * 100).toFixed(1);

        const seg = document.createElement('div');
        seg.className = 'spectrum-segment';
        seg.style.width = `${pct}%`;
        seg.style.backgroundColor = meta.color;
        seg.title = `${displayName}: ${formatBytes(cat.total_size_bytes)} (${pct}%) - 点击查看详情`;
        seg.onclick = () => openInspectorByCategory(cat.id);
        container.appendChild(seg);

        const leg = document.createElement('div');
        leg.className = 'spectrum-legend-item';
        leg.title = `点击排查 ${displayName}`;
        leg.onclick = () => openInspectorByCategory(cat.id);
        leg.innerHTML = `
          <span class="spectrum-color-dot" style="background-color: ${meta.color};"></span>
          <span>${displayName}: <strong style="color: #ffffff;">${formatBytes(cat.total_size_bytes)}</strong> <span style="opacity: 0.7; font-size: 10.5px; font-family: var(--font-mono);">(${pct}%)</span></span>
        `;
        legendGrid.appendChild(leg);
      });
    }

    function renderGiantTreemap(files) {
      const canvas = document.getElementById('giantTreemapCanvas');
      const countEl = document.getElementById('treemapSubtitleCount');
      if (!canvas) return;

      if (!files || files.length === 0) {
        canvas.innerHTML = '<div style="grid-column: span 12; grid-row: span 6; display: flex; align-items: center; justify-content: center; color: var(--text-tertiary); font-size: 13px;">暂未检索到 100MB+ 巨型资产</div>';
        if (countEl) countEl.innerText = '0';
        return;
      }

      if (countEl) countEl.innerText = files.length;
      canvas.innerHTML = '';

      const sorted = [...files].sort((a, b) => b.size_bytes - a.size_bytes);
      const totalBytes = sorted.reduce((sum, f) => sum + f.size_bytes, 0);

      const gridSpans = [
        { col: 5, row: 6 },
        { col: 4, row: 4 },
        { col: 3, row: 3 },
        { col: 3, row: 3 },
        { col: 4, row: 2 }
      ];

      const getStyleForFile = (f) => {
        const ext = (f.extension || '').toLowerCase();
        const cat = (f.category || '').toLowerCase();
        const name = (f.name || '').toLowerCase();

        if (cat.includes('database') || ext === 'db' || ext === 'sqlite' || ext === 'vscdb' || ext === 'wal' || name.includes('.db') || name.includes('.vscdb') || name.includes('sqlite') || name.includes('-wal')) {
          return {
            label: '数据库',
            bg: 'linear-gradient(135deg, rgba(6,182,212,0.35) 0%, rgba(14,116,144,0.55) 100%)',
            border: 'rgba(6,182,212,0.5)',
            badgeBg: 'rgba(6,182,212,0.22)',
            badgeColor: '#67e8f9',
            advice: 'SQLite 数据库 · 建议原生 VACUUM 收缩'
          };
        }
        if (cat.includes('virtual') || ext === 'img' || ext === 'vmdk' || ext === 'qcow2' || ext === 'vhd' || ext === 'vhdx' || name.includes('.img')) {
          return {
            label: '虚拟机磁盘',
            bg: 'linear-gradient(135deg, rgba(168,85,247,0.35) 0%, rgba(126,34,206,0.55) 100%)',
            border: 'rgba(168,85,247,0.5)',
            badgeBg: 'rgba(168,85,247,0.22)',
            badgeColor: '#d8b4fe',
            advice: '虚拟机虚拟盘 · 建议使用 NTFS 符号链接搬家至副盘'
          };
        }
        if (ext === 'dmp' || ext === 'sys' || name.includes('ram.img')) {
          return {
            label: '系统与快照',
            bg: 'linear-gradient(135deg, rgba(99,102,241,0.35) 0%, rgba(67,56,202,0.55) 100%)',
            border: 'rgba(99,102,241,0.5)',
            badgeBg: 'rgba(99,102,241,0.22)',
            badgeColor: '#a5b4fc',
            advice: '快照与系统转储 · 可视需求清理或随主目录迁移'
          };
        }
        if (cat.includes('installer') || cat.includes('executable') || ext === 'exe' || ext === 'msi') {
          return {
            label: '安装包程序',
            bg: 'linear-gradient(135deg, rgba(245,158,11,0.35) 0%, rgba(180,83,9,0.55) 100%)',
            border: 'rgba(245,158,11,0.5)',
            badgeBg: 'rgba(245,158,11,0.22)',
            badgeColor: '#fcd34d',
            advice: '安装包与可执行程序 · 建议核验后清理或归档'
          };
        }
        if (cat.includes('archive') || ext === 'zip' || ext === 'rar' || ext === '7z' || ext === 'tar') {
          return {
            label: '压缩归档',
            bg: 'linear-gradient(135deg, rgba(59,130,246,0.35) 0%, rgba(29,78,216,0.55) 100%)',
            border: 'rgba(59,130,246,0.5)',
            badgeBg: 'rgba(59,130,246,0.22)',
            badgeColor: '#93c5fd',
            advice: '历史压缩归档 · 建议核实后安全清理'
          };
        }
        return {
          label: '沉淀大资产',
          bg: 'linear-gradient(135deg, rgba(71,85,105,0.45) 0%, rgba(30,41,59,0.65) 100%)',
          border: 'rgba(100,116,139,0.5)',
          badgeBg: 'rgba(100,116,139,0.22)',
          badgeColor: '#cbd5e1',
          advice: '沉淀大资产 · 可定位目录查看'
        };
      };

      const topCount = Math.min(sorted.length, 5);
      for (let i = 0; i < topCount; i++) {
        const file = sorted[i];
        const span = gridSpans[i] || { col: 3, row: 3 };
        const styleMeta = getStyleForFile(file);
        const pct = ((file.size_bytes / (totalBytes || 1)) * 100).toFixed(1);

        const cell = document.createElement('div');
        cell.className = 'treemap-cell';
        cell.style.gridColumn = `span ${span.col}`;
        cell.style.gridRow = `span ${span.row}`;
        cell.style.background = styleMeta.bg;
        cell.style.border = `1px solid ${styleMeta.border}`;

        const pathParts = file.path.split(/[\\/]/);
        const folderPart = pathParts.length > 2 ? pathParts.slice(-3, -1).join('/') : '';

        cell.innerHTML = `
          <div class="treemap-cell-top">
            <span class="treemap-cell-badge" style="background: ${styleMeta.badgeBg}; color: ${styleMeta.badgeColor};">
              ${styleMeta.label} ${formatBytes(file.size_bytes)}
            </span>
            <div class="treemap-cell-name" title="${escapeHtml(file.name)}">${escapeHtml(file.name)}</div>
            <div class="treemap-cell-path" title="${escapeHtml(file.path)}">${escapeHtml(folderPart)}</div>
          </div>
          <div class="treemap-cell-bottom">
            <span style="opacity: 0.85; font-size: 10.5px;">占大资产 ${pct}%</span>
            <span style="font-size: 10.5px; color: ${styleMeta.badgeColor}; font-weight: 600;">点击透视</span>
          </div>
        `;

        cell.onmouseenter = () => updateTreemapInspector(file, pct, styleMeta);
        cell.onclick = () => {
          document.querySelectorAll('.treemap-cell').forEach(c => c.classList.remove('active-selected'));
          cell.classList.add('active-selected');
          updateTreemapInspector(file, pct, styleMeta);
          highlightAndScrollToGiantFile(file.path);
        };

        canvas.appendChild(cell);
      }

      if (sorted.length > 0) {
        const topFile = sorted[0];
        const topPct = ((topFile.size_bytes / (totalBytes || 1)) * 100).toFixed(1);
        updateTreemapInspector(topFile, topPct, getStyleForFile(topFile));
      }
    }

    function updateTreemapInspector(file, pct, styleMeta) {
      const nameEl = document.getElementById('treemapDetailName');
      const sizeEl = document.getElementById('treemapDetailSize');
      const catEl = document.getElementById('treemapDetailCategory');
      const pathEl = document.getElementById('treemapDetailPath');
      const adviceEl = document.getElementById('treemapDetailAdvice');
      const actionsEl = document.getElementById('treemapDetailActions');

      if (nameEl) nameEl.innerText = file.name;
      if (sizeEl) sizeEl.innerText = `${formatBytes(file.size_bytes)} (${pct}%)`;
      if (catEl) {
        catEl.innerText = styleMeta.label;
        catEl.style.backgroundColor = styleMeta.badgeBg;
        catEl.style.color = styleMeta.badgeColor;
      }
      if (pathEl) {
        pathEl.innerText = file.path;
        pathEl.title = file.path;
      }
      if (adviceEl) adviceEl.innerText = styleMeta.advice;

      if (actionsEl) {
        const ext = (file.extension || '').toLowerCase();
        const isDb = ext === 'db' || ext === 'sqlite' || ext === 'vscdb' || file.name.includes('.vscdb') || file.name.includes('.db');
        const isVm = ext === 'img' || ext === 'vmdk' || ext === 'qcow2' || file.name.includes('.img');

        let extraBtn = '';
        if (isDb) {
          extraBtn = `<button class="btn btn-primary" style="padding: 2px 10px; font-size: 11px;" onclick="openInspectorByCategory('sqlite_optimize')">VACUUM 压缩</button>`;
        } else if (isVm) {
          extraBtn = `<button class="btn btn-primary" style="padding: 2px 10px; font-size: 11px;" onclick="switchTab('tools')">Junction 搬家</button>`;
        }

        actionsEl.innerHTML = `
          ${extraBtn}
          <button class="btn btn-secondary" style="padding: 2px 10px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(file.path)}')">定位目录</button>
          <button class="btn btn-secondary" style="padding: 2px 10px; font-size: 11px;" onclick="copyTextToClipboard('${escapeHtml(file.path)}')">复制绝对路径</button>
        `;
      }
    }

    function highlightAndScrollToGiantFile(targetPath) {
      const rows = document.querySelectorAll('#giantFilesTableBody tr');
      rows.forEach(r => {
        if (r.getAttribute('data-path') === targetPath) {
          r.classList.add('selected');
          r.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
          r.classList.remove('selected');
        }
      });
    }

    function copyTextToClipboard(text) {
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => showToast('已成功复制绝对路径到剪贴板'));
      } else {
        showToast('已复制路径: ' + text);
      }
    }

    // Junction Migration
    async function loadActiveJunctions() {
      try {
        const res = await fetch('/api/junctions');
        const list = await res.json();
        const container = document.getElementById('toolsJunctionList');
        if (container) {
          if (list.length === 0) {
            container.innerHTML = '<div style="padding: 12px 0; color: var(--text-tertiary); text-align: center;">当前系统未创建任何活动 NTFS 符号链接 (Junction)</div>';
          } else {
            let html = '<table class="data-grid"><thead><tr><th>原始路径 (C盘)</th><th>物理重定向路径</th><th>建立时间</th><th style="width:140px; text-align:center;">操作</th></tr></thead><tbody>';
            list.forEach(j => {
              html += `
                <tr>
                  <td><span class="path-text" title="${escapeHtml(j.source_path)}">${escapeHtml(j.source_path)}</span></td>
                  <td><span class="path-text" title="${escapeHtml(j.target_path)}" style="color: #60cdff;">${escapeHtml(j.target_path)}</span></td>
                  <td style="color: var(--text-tertiary);">${escapeHtml(j.created_at || '最近')}</td>
                  <td style="text-align: center;">
                    <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(j.target_path)}')">定位</button>
                    <button class="btn btn-danger" style="padding: 2px 8px; font-size: 11px; margin-left: 4px;" onclick="rollbackJunction('${escapeHtml(j.source_path)}')">还原</button>
                  </td>
                </tr>
              `;
            });
            html += '</tbody></table>';
            container.innerHTML = html;
          }
        }
        const tbody = document.getElementById('activeJunctionsTableBody');
        if (tbody) {
          tbody.innerHTML = '';
          if (list.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 24px; color: var(--text-tertiary);">当前尚未创建任何活动软联接</td></tr>`;
          } else {
            list.forEach(j => {
              const tr = document.createElement('tr');
              tr.innerHTML = `
                <td style="font-family: var(--font-mono);"><span class="path-text" title="${escapeHtml(j.source_path)}">${escapeHtml(j.source_path)}</span></td>
                <td style="font-family: var(--font-mono); color: #60cdff;"><span class="path-text" title="${escapeHtml(j.target_path)}">${escapeHtml(j.target_path)}</span></td>
                <td style="color: var(--text-tertiary);">${escapeHtml(j.created_at || '最近')}</td>
                <td style="text-align: center; display: flex; gap: 6px; justify-content: center;">
                  <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(j.target_path)}')">打开目标</button>
                  <button class="btn btn-danger" style="padding: 2px 8px; font-size: 11px;" onclick="rollbackJunction('${escapeHtml(j.source_path)}')">安全还原</button>
                </td>
              `;
              tbody.appendChild(tr);
            });
          }
        }
      } catch (e) {
        console.error('Failed to load junctions', e);
      }
    }

    function escapeJsString(s) {
      return (s || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    }

    function formatUnixTimestamp(ts) {
      if (!ts) return '-';
      const num = parseInt(ts, 10);
      if (isNaN(num)) return ts;
      const d = new Date(num * 1000);
      return d.getFullYear() + '-' +
        String(d.getMonth() + 1).padStart(2, '0') + '-' +
        String(d.getDate()).padStart(2, '0') + ' ' +
        String(d.getHours()).padStart(2, '0') + ':' +
        String(d.getMinutes()).padStart(2, '0') + ':' +
        String(d.getSeconds()).padStart(2, '0');
    }

    // High-Value Migration Presets (Pillar 1)
    const MIGRATION_PRESETS = [
      { name: 'Ollama 本地模型', path: 'C:\\Users\\EDY\\.ollama\\models', note: 'AI 核心资产' },
      { name: 'HuggingFace 权重', path: 'C:\\Users\\EDY\\.cache\\huggingface\\hub', note: 'AI 缓存' },
      { name: 'PyTorch Hub 模型', path: 'C:\\Users\\EDY\\.cache\\torch\\hub', note: 'AI 权重' },
      { name: 'Steam 游戏库', path: 'C:\\Program Files (x86)\\Steam\\steamapps\\common', note: '大型游戏' },
      { name: 'Unity Hub 编辑器', path: 'C:\\Program Files\\Unity\\Hub\\Editor', note: '游戏引擎' },
      { name: 'VS 安装包缓存', path: 'C:\\ProgramData\\Microsoft\\VisualStudio\\Packages', note: '开发套件' },
      { name: '微信聊天资产', path: 'C:\\Users\\EDY\\Documents\\WeChat Files', note: '聊天附件' },
      { name: 'Android SDK', path: 'C:\\Users\\EDY\\AppData\\Local\\Android\\Sdk', note: '移动端开发' }
    ];

    let migrationPollTimer = null;

    function openMigrationWizardModal() {
      const modal = document.getElementById('migrationWizardModal');
      if (!modal) return;

      // Populate Target Drive Options from available disks
      const driveSelect = document.getElementById('customMigrateTargetDrive');
      if (driveSelect) {
        driveSelect.innerHTML = '';
        const nonCDrives = (state.disks || []).filter(d => d.letter.toUpperCase() !== 'C');
        const candidateDrives = nonCDrives.length > 0 ? nonCDrives : (state.disks || []);
        candidateDrives.forEach(d => {
          const opt = document.createElement('option');
          opt.value = d.letter;
          opt.textContent = `${d.letter}: 驱动器 (剩余 ${formatBytes(d.free_bytes)} / 共 ${formatBytes(d.total_bytes)})`;
          driveSelect.appendChild(opt);
        });
      }

      // Render preset tags
      renderMigrationPresets();

      // Reset fields
      const srcInput = document.getElementById('customMigrateSource');
      if (srcInput) srcInput.value = '';
      const card = document.getElementById('migratePathInspectionCard');
      if (card) card.innerHTML = '<div style="color:var(--text-tertiary);">请输入待搬迁路径或点击上方预设开始健康检测...</div>';
      const progressBox = document.getElementById('migrationProgressContainer');
      if (progressBox) progressBox.style.display = 'none';
      const startBtn = document.getElementById('startMigrationBtn');
      if (startBtn) startBtn.disabled = false;

      modal.classList.add('active');
    }

    function closeMigrationWizardModal() {
      const modal = document.getElementById('migrationWizardModal');
      if (modal) modal.classList.remove('active');
      if (migrationPollTimer) {
        clearInterval(migrationPollTimer);
        migrationPollTimer = null;
      }
    }

    function renderMigrationPresets() {
      const container = document.getElementById('migrationPresetTags');
      if (!container) return;
      container.innerHTML = '';
      MIGRATION_PRESETS.forEach(p => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-secondary';
        btn.style.padding = '3px 8px';
        btn.style.fontSize = '11px';
        btn.innerHTML = `<span style="font-weight:600; color:#fff;">${escapeHtml(p.name)}</span> <span style="color:var(--text-tertiary); font-size:10px;">(${escapeHtml(p.note)})</span>`;
        btn.onclick = () => selectMigrationPreset(p.path);
        container.appendChild(btn);
      });
    }

    function selectMigrationPreset(presetPath) {
      const srcInput = document.getElementById('customMigrateSource');
      if (srcInput) {
        srcInput.value = presetPath;
        analyzeCustomMigrationPath();
      }
    }

    let migrateInputDebounce = null;
    function onMigrateSourceInput() {
      if (migrateInputDebounce) clearTimeout(migrateInputDebounce);
      migrateInputDebounce = setTimeout(() => {
        analyzeCustomMigrationPath();
      }, 500);
    }

    async function analyzeCustomMigrationPath() {
      const src = (document.getElementById('customMigrateSource')?.value || '').trim();
      const card = document.getElementById('migratePathInspectionCard');
      if (!src) {
        if (card) card.innerHTML = '<div style="color:var(--text-tertiary);">请输入待搬迁路径或点击上方预设开始健康检测...</div>';
        return;
      }

      if (card) card.innerHTML = '<div style="color:var(--text-secondary);">正在对目标目录执行互斥进程扫描与体积预检...</div>';

      try {
        const res = await fetch('/api/check-path', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: src })
        });
        const data = await res.json();
        if (!data.exists) {
          if (card) card.innerHTML = `
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:10px; color:var(--text-tertiary);">
              <div style="font-weight:600; color:#fff; margin-bottom:2px;">未检测到物理目录</div>
              <div>指定路径当前在系统中不存在或尚未生成缓存。若应用刚安装，可在首次运行后再执行搬迁。</div>
            </div>
          `;
          return;
        }

        if (data.is_junction) {
          if (card) card.innerHTML = `
            <div style="background:rgba(0,120,212,0.12); border:1px solid rgba(0,120,212,0.3); border-radius:var(--radius-sm); padding:10px; color:#60cdff;">
              <div style="font-weight:600; margin-bottom:2px;">已是系统虚拟联接 (Junction)</div>
              <div>该目录已经成功建立了符号重定向，物理数据已存储在从盘，无需重复迁移。</div>
            </div>
          `;
          return;
        }

        const locks = data.locking_processes || [];
        if (locks.length > 0) {
          let lockButtons = locks.map(p => `
            <span class="tag-pill" style="background:rgba(255,255,255,0.08); color:#fff; display:inline-flex; align-items:center; gap:6px; padding:3px 8px; margin:2px;">
              <span>${escapeHtml(p.name)} (PID: ${p.pid})</span>
              <button class="btn btn-danger" style="padding:1px 6px; font-size:10px;" onclick="killLockingProcess('${escapeJsString(p.name)}')">结束</button>
            </span>
          `).join('');

          if (card) card.innerHTML = `
            <div style="background:rgba(255,153,164,0.1); border:1px solid rgba(255,153,164,0.3); border-radius:var(--radius-sm); padding:10px; color:#ff99a4;">
              <div style="font-weight:600; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
                <span class="status-dot-pulse" style="background:#ff99a4;"></span>
                <span>互斥进程告警: 检测到 ${locks.length} 个运行中的程序正在占用此目录</span>
              </div>
              <div style="font-size:11.5px; color:var(--text-secondary); margin-bottom:8px;">
                为保障数据完整性并防止写入中断，搬迁前必须退出占用应用。您可以手动退出或点击下方快捷结束：
              </div>
              <div style="display:flex; flex-wrap:wrap; gap:4px;">${lockButtons}</div>
            </div>
          `;
        } else {
          if (card) card.innerHTML = `
            <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25); border-radius:var(--radius-sm); padding:10px; color:#22c55e;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:6px; font-weight:600;">
                  <span class="icon" style="width:14px; height:14px;"><svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                  <span>预检互斥通过：无活跃进程独占此目录</span>
                </div>
                <span class="tag-pill tag-blue" style="font-size:11px;">${formatBytes(data.size_bytes)} (${data.file_count} 个文件)</span>
              </div>
              <div style="font-size:11.5px; color:var(--text-secondary); margin-top:4px;">
                资产已就绪，搬迁过程中支持随时安全原子回滚。
              </div>
            </div>
          `;
        }
      } catch (e) {
        if (card) card.innerHTML = `<div style="color:var(--status-danger);">预检异常: ${escapeHtml(e.message)}</div>`;
      }
    }

    async function killLockingProcess(procName) {
      try {
        const res = await fetch('/api/kill-process', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: procName })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`已结束占用进程: ${procName}`);
          setTimeout(() => analyzeCustomMigrationPath(), 600);
        } else {
          showToast(`结束进程失败: ${data.error || '权限不足'}`);
        }
      } catch (e) {
        showToast(`操作失败: ${e.message}`);
      }
    }

    function executeCustomMigration() {
      const src = (document.getElementById('customMigrateSource')?.value || '').trim();
      const targetDrive = document.getElementById('customMigrateTargetDrive')?.value;
      if (!src) {
        showToast('请填写需要搬迁的源目录绝对路径');
        return;
      }
      if (!targetDrive) {
        showToast('请选择目标驱动器');
        return;
      }

      openConfirmModal('Junction 虚拟化搬家确认', `即将把目录 <br><b>${escapeHtml(src)}</b><br> 完整搬迁至 <b>${targetDrive}: 盘</b>，并在原位自动创建 NTFS Junction。<br><br>所有软件、快捷方式均不受影响，完全无感照常运行。`, async () => {
        closeConfirmModal();

        const progressContainer = document.getElementById('migrationProgressContainer');
        const progressBar = document.getElementById('migrationProgressBar');
        const percentLabel = document.getElementById('migrationPercentLabel');
        const statusLabel = document.getElementById('migrationStatusLabel');
        const startBtn = document.getElementById('startMigrationBtn');

        if (progressContainer) progressContainer.style.display = 'block';
        if (startBtn) startBtn.disabled = true;
        if (progressBar) progressBar.style.width = '2%';
        if (percentLabel) percentLabel.innerText = '准备中...';
        if (statusLabel) statusLabel.innerText = '正在初始化底层传输与建立事务快照...';

        try {
          const res = await fetch('/api/migrate-start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_path: src, target_drive: targetDrive })
          });
          const data = await res.json();
          if (!data.success) {
            showToast('启动搬迁任务失败: ' + (data.error || '未知错误'));
            if (progressContainer) progressContainer.style.display = 'none';
            if (startBtn) startBtn.disabled = false;
            return;
          }

          // Polling migration status
          migrationPollTimer = setInterval(async () => {
            try {
              const statusRes = await fetch('/api/migrate-status');
              const status = await statusRes.json();

              if (progressBar) progressBar.style.width = `${Math.min(100, Math.max(0, status.percent))}%`;
              if (percentLabel) percentLabel.innerText = `${status.percent.toFixed(1)}%`;
              if (statusLabel) statusLabel.innerText = status.current_file || '正在传输...';

              if (status.state === 'COMPLETED') {
                clearInterval(migrationPollTimer);
                migrationPollTimer = null;
                if (progressBar) progressBar.style.width = '100%';
                if (percentLabel) percentLabel.innerText = '100%';
                if (statusLabel) statusLabel.innerText = '搬迁完成! 已建立透明符号联接';

                showToast(`搬迁成功！已在原位建立 NTFS Junction`);
                setTimeout(() => {
                  closeMigrationWizardModal();
                  loadActiveJunctions();
                  refreshDisks();
                  runScan();
                }, 1200);
              } else if (status.state === 'FAILED') {
                clearInterval(migrationPollTimer);
                migrationPollTimer = null;
                showToast(`搬迁失败: ${status.error_msg || '未知错误'}`);
                if (statusLabel) statusLabel.innerText = `失败: ${status.error_msg || '未知错误'}`;
                if (startBtn) startBtn.disabled = false;
              }
            } catch (e) {
              console.error('获取搬迁进度异常', e);
            }
          }, 600);
        } catch (e) {
          showToast('搬迁启动请求异常: ' + e.message);
          if (progressContainer) progressContainer.style.display = 'none';
          if (startBtn) startBtn.disabled = false;
        }
      });
    }

    async function rollbackJunction(src) {
      openConfirmModal('还原 Junction 联接确认', `确定要将软链接还原回原始 C: 盘真实目录吗？`, async () => {
        closeConfirmModal();
        showToast('正在还原数据并解绑软链接...');
        try {
          const res = await fetch('/api/junctions/rollback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_path: src })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`已成功还原原始目录！`);
            loadActiveJunctions();
            refreshDisks();
          } else {
            showToast('还原失败: ' + data.error);
          }
        } catch (e) {
          showToast('还原异常: ' + e.message);
        }
      });
    }

    // Common Actions
    async function revealInExplorer(p) {
      try {
        await fetch('/api/reveal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: p })
        });
        showToast('已在文件资源管理器中定位');
      } catch (e) {
        showToast('定位失败: ' + e.message);
      }
    }

    async function deleteSingleItem(p) {
      openConfirmModal('清理删除确认', `确定要安全清理此项吗？<br><br><span style="font-family:var(--font-mono); font-size:11px; color:#ff99a4;">${escapeHtml(p)}</span>`, async () => {
        closeConfirmModal();
        showToast('正在清理...');
        try {
          const res = await fetch('/api/delete-file', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: p })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`清理成功，释放 ${formatBytes(data.bytes_freed)}`);
            runScan();
            refreshDisks();
            toggleInspector(false);
          } else {
            showToast('清理失败，文件可能被独占');
          }
        } catch (e) {
          showToast('清理请求失败: ' + e.message);
        }
      });
    }

    function executeCleanSelected() {
      if (state.selectedPaths.size === 0) {
        showToast('请先选择至少一项需要清理的资产');
        return;
      }
      openConfirmModal('批量清理确认', `确定要立即清理当前已选中的 <b>${state.selectedPaths.size}</b> 项冗余资产吗？`, async () => {
        closeConfirmModal();
        showToast('正在执行极速安全清理...');
        try {
          const res = await fetch('/api/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paths: Array.from(state.selectedPaths) })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`清理成功！释放 ${formatBytes(data.bytes_freed)}，删除 ${data.files_deleted} 个文件`);
            runScan();
            refreshDisks();
          } else {
            showToast('清理完成，部分文件被独占');
          }
        } catch (e) {
          showToast('请求异常: ' + e.message);
        }
      });
    }

    function cleanCategoryItems(catId) {
      const paths = [];
      if (state.scanReport) {
        const cat = state.scanReport.categories.find(c => c.id === catId);
        if (cat) {
          cat.rules.forEach(r => {
            r.matched_paths.forEach(mp => {
              if (mp.size_bytes > 0) paths.push(mp.path);
            });
          });
        }
      }
      if (paths.length === 0) {
        showToast('当前分类暂无可清理项目');
        return;
      }
      openConfirmModal('专项清理确认', `即将清理该分类下的 ${paths.length} 个缓存目录，确认继续吗？`, async () => {
        closeConfirmModal();
        showToast('正在清理...');
        try {
          const res = await fetch('/api/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paths })
          });
          const data = await res.json();
          showToast(`专项清理完成，释放 ${formatBytes(data.bytes_freed)}`);
          runScan();
          refreshDisks();
        } catch (e) {
          showToast('清理异常: ' + e.message);
        }
      });
    }

    async function vacuumDatabase(p) {
      showToast('正在执行 SQLite VACUUM 碎片无损收缩...');
      try {
        const res = await fetch('/api/vacuum', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ db_path: p })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`收缩完成！释放 ${formatBytes(data.bytes_freed)}`);
          runScan();
          refreshDisks();
        } else {
          showToast('VACUUM 失败: ' + data.error);
        }
      } catch (e) {
        showToast('VACUUM 异常: ' + e.message);
      }
    }

    // Custom Rules Engine
    function renderCustomRulesTable() {
      const tbody = document.getElementById('customRulesTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      if (!state.scanReport || !state.scanReport.categories) return;

      const sortedCats = [...state.scanReport.categories].sort((a, b) => {
        if (a.id === 'custom') return -1;
        if (b.id === 'custom') return 1;
        return 0;
      });

      sortedCats.forEach(cat => {
        cat.rules.forEach(rule => {
          const tr = document.createElement('tr');
          tr.setAttribute('data-name', rule.name);
          tr.onclick = () => {
            document.querySelectorAll('.data-grid tbody tr').forEach(r => r.classList.remove('selected'));
            tr.classList.add('selected');
            inspectItem({ name: rule.name, path: rule.path_pattern || '-', size_bytes: rule.total_size_bytes || 0, category: cat.name });
          };
          tr.innerHTML = `
            <td><span class="badge-pill badge-safe">${escapeHtml(cat.name)}</span></td>
            <td style="font-weight:600;">${escapeHtml(rule.name)}</td>
            <td><span class="path-text" title="${escapeHtml(rule.path_pattern || '')}">${escapeHtml(rule.path_pattern || '')}</span></td>
            <td style="text-align: center;"><span class="badge-pill ${rule.matched_paths && rule.matched_paths.length > 0 ? 'badge-junction' : 'badge-openwith'}">${rule.matched_paths && rule.matched_paths.length > 0 ? `匹配 ${rule.matched_paths.length} 处` : '监听中'}</span></td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    async function submitCustomRule() {
      const name = document.getElementById('ruleNameInput').value.trim();
      const pattern = document.getElementById('rulePatternInput').value.trim();
      if (!name || !pattern) {
        showToast('请完整填写规则名称与路径模式');
        return;
      }
      showToast('正在保存规则并重新编译规则库...');
      try {
        const res = await fetch('/api/rules/custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, path_pattern: pattern })
        });
        const data = await res.json();
        if (data.success) {
          showToast('规则已保存并注入引擎');
          document.getElementById('ruleNameInput').value = '';
          document.getElementById('rulePatternInput').value = '';
          await runScan();
          renderCustomRulesTable();
        } else {
          showToast(`保存失败: ${data.error || '未知错误'}`);
        }
      } catch (e) {
        showToast('保存规则网络请求失败: ' + e.message);
      }
    }

    // Modal
    let onConfirmCallback = null;
    function openConfirmModal(title, body, okCb) {
      document.getElementById('confirmModalTitle').innerText = title;
      document.getElementById('confirmModalBody').innerHTML = body;
      onConfirmCallback = okCb;
      document.getElementById('confirmModal').classList.add('active');
    }
    function closeConfirmModal() {
      document.getElementById('confirmModal').classList.remove('active');
      onConfirmCallback = null;
    }
    function onConfirmModalOk() {
      if (onConfirmCallback) onConfirmCallback();
    }

    // Window controls
    function minimizeWindow() { showToast('快捷键: Win+Down 可最小化本窗口'); }
    function maximizeWindow() { showToast('快捷键: Win+Up 可最大化本窗口'); }
    async function shutdownApp() {
      openConfirmModal('退出软件', '确定要退出 CleanFlow Pro 智能空间管家吗？', async () => {
        try { await fetch('/api/shutdown', { method: 'POST' }); } catch (e) {}
        window.close();
      });
    }

    // ==========================================
    // Listary Feature A: Spotlight Floating Bar
    // ==========================================
    let spotlightHits = [];
    let spotlightSelectedIndex = 0;
    let spotlightTimer = null;
    let spotlightCurrentCategory = 'all';
    let queryHistoryList = [];
    let queryHistoryIndex = -1;
    let spotlightIsShowingRecent = false;

    async function loadSpotlightHistoryQueries() {
      try {
        const res = await fetch('/api/history/queries');
        if (res.ok) {
          queryHistoryList = await res.json();
          queryHistoryIndex = -1;
        }
      } catch (e) {
        console.warn('加载检索词历史失败:', e);
      }
    }

    async function loadRecentSpotlightFiles() {
      const container = document.getElementById('spotlightResultsContainer');
      const statusText = document.getElementById('spotlightStatusText');
      if (!container) return;
      try {
        const res = await fetch('/api/history/recent');
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        let items = data || [];

        if (spotlightCurrentCategory !== 'all') {
          items = items.filter(it => {
            const name = (it.file_name || it.path || '').toLowerCase();
            const ext = name.includes('.') ? name.split('.').pop() : '';
            if (spotlightCurrentCategory === 'folder') return it.is_dir;
            if (spotlightCurrentCategory === 'doc') return ['txt', 'md', 'doc', 'docx', 'pdf', 'xlsx', 'xls', 'pptx', 'ppt', 'csv', 'json', 'yaml', 'toml', 'xml', 'log'].includes(ext);
            if (spotlightCurrentCategory === 'pic') return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg', 'ico', 'tiff', 'psd'].includes(ext);
            if (spotlightCurrentCategory === 'video') return ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm', 'm4v'].includes(ext);
            if (spotlightCurrentCategory === 'audio') return ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'wma'].includes(ext);
            if (spotlightCurrentCategory === 'archive') return ['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'iso'].includes(ext);
            if (spotlightCurrentCategory === 'app') return ['exe', 'msi', 'bat', 'cmd', 'ps1', 'lnk'].includes(ext);
            return true;
          });
        }

        spotlightHits = items.map(it => ({
          name: it.file_name || it.path,
          path: it.path,
          is_dir: it.is_dir,
          size_bytes: 0,
          detail: `历史访问: ${it.access_count} 次 · ${it.accessed_at || '近期'}`,
          is_recent: true
        }));
        spotlightSelectedIndex = 0;
        spotlightIsShowingRecent = true;

        if (statusText) {
          statusText.innerText = items.length > 0 
            ? `最近打开与历史访问 (${items.length} 项) · ↑↓ 翻看检索词历史，回车快速打开`
            : '输入关键词或拼音首字母即刻全盘毫秒检索 · 上下键选择 · 回车打开 · Tab 动作流水线';
        }
        renderSpotlightHits();
      } catch (e) {
        console.warn('加载最近文件历史失败:', e);
      }
    }

    function selectSpotlightCategory(cat) {
      spotlightCurrentCategory = cat;
      const chips = document.querySelectorAll('#spotlightChipsRow .spotlight-chip');
      chips.forEach(c => {
        if (c.getAttribute('data-cat') === cat) {
          c.classList.add('active');
        } else {
          c.classList.remove('active');
        }
      });
      const input = document.getElementById('spotlightInput');
      const query = input ? input.value.trim() : '';
      if (query) {
        executeSpotlightSearch(query);
      } else {
        loadRecentSpotlightFiles();
      }
    }

    function openSpotlight() {
      const overlay = document.getElementById('spotlightOverlay');
      const input = document.getElementById('spotlightInput');
      if (!overlay || !input) return;
      overlay.style.display = 'flex';
      input.value = '';
      input.focus();
      spotlightCurrentCategory = 'all';
      const chips = document.querySelectorAll('#spotlightChipsRow .spotlight-chip');
      chips.forEach(c => {
        if (c.getAttribute('data-cat') === 'all') c.classList.add('active');
        else c.classList.remove('active');
      });
      spotlightHits = [];
      spotlightSelectedIndex = 0;
      queryHistoryIndex = -1;
      loadSpotlightHistoryQueries();
      loadRecentSpotlightFiles();
    }

    function closeSpotlight() {
      const overlay = document.getElementById('spotlightOverlay');
      if (overlay) overlay.style.display = 'none';
    }

    function handleSpotlightOverlayClick(e) {
      if (e.target && e.target.id === 'spotlightOverlay') {
        closeSpotlight();
      }
    }

    function onSpotlightInput(val) {
      if (spotlightTimer) clearTimeout(spotlightTimer);
      const query = val.trim();
      if (!query) {
        queryHistoryIndex = -1;
        loadRecentSpotlightFiles();
        return;
      }
      queryHistoryIndex = -1;
      spotlightTimer = setTimeout(() => {
        executeSpotlightSearch(query);
      }, 90);
    }

    async function executeSpotlightSearch(query) {
      const container = document.getElementById('spotlightResultsContainer');
      const statusText = document.getElementById('spotlightStatusText');
      if (!container) return;
      spotlightIsShowingRecent = false;
      try {
        const isGrep = query.startsWith('grep:') || query.startsWith('sym:');
        let effectiveQuery = query;
        if (!isGrep && !devNoiseShieldEnabled && !query.includes('shield:')) {
          effectiveQuery = query + ' shield:0';
        }
        let endpoint = isGrep
          ? ('/api/search/grep?q=' + encodeURIComponent(effectiveQuery))
          : ('/api/search/query?q=' + encodeURIComponent(effectiveQuery));

        if (!isGrep && spotlightCurrentCategory && spotlightCurrentCategory !== 'all') {
          endpoint += (endpoint.includes('?') ? '&' : '?') + 'category=' + encodeURIComponent(spotlightCurrentCategory);
        }

        const res = await fetch(endpoint);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        
        if (isGrep) {
          spotlightHits = (data.hits || []).slice(0, 15).map(h => ({
            name: `${h.file_name}:${h.line_number}`,
            path: h.file_path,
            is_dir: false,
            size_bytes: 0,
            detail: h.line_content || ''
          }));
        } else {
          spotlightHits = (data.hits || []).slice(0, 15);
        }

        if (data.launcher_hit) {
          spotlightHits.unshift({
            is_launcher: true,
            name: data.launcher_hit.title,
            path: data.launcher_hit.target,
            detail: data.launcher_hit.description,
            action_type: data.launcher_hit.action_type,
            shortcut_label: data.launcher_hit.shortcut_label,
            is_dir: false
          });
        }

        spotlightSelectedIndex = 0;
        if (statusText) {
          statusText.innerText = `命中 ${data.total_hits || spotlightHits.length} 项 (上下键选择, 回车打开/直达, Tab 动作, Ctrl+G 跳转)`;
        }
        renderSpotlightHits();
      } catch (e) {
        container.innerHTML = `<div style="padding:16px; color:var(--status-danger); text-align:center;">检索出错: ${escapeHtml(e.message)}</div>`;
      }
    }

    function renderSpotlightHits() {
      const container = document.getElementById('spotlightResultsContainer');
      if (!container) return;
      if (spotlightHits.length === 0) {
        const emptyMsg = spotlightIsShowingRecent 
          ? '暂无最近打开历史 · 输入关键词或拼音首字母即可全盘检索'
          : '未找到匹配结果 (支持全拼、声母首字母如 jsq/wx, 1-edit 容错纠错)';
        container.innerHTML = `<div style="padding: 24px; text-align: center; color: var(--text-tertiary); font-size: 13px;">${emptyMsg}</div>`;
        return;
      }
      container.innerHTML = spotlightHits.map((h, idx) => {
        const isSelected = idx === spotlightSelectedIndex;
        if (h.is_launcher) {
          return `
            <div class="spotlight-item ${isSelected ? 'selected' : ''}" style="background: rgba(96, 205, 255, 0.12); border: 1px solid rgba(96, 205, 255, 0.35);" onclick="selectAndExecuteSpotlightHit(${idx})">
              <div class="spotlight-item-left">
                <svg style="width:16px;height:16px;fill:#60cdff;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
                <div style="display:flex; flex-direction:column; overflow:hidden;">
                  <div class="spotlight-item-name" style="color:#60cdff; font-weight:700;">${escapeHtml(h.name)} · [${escapeHtml(h.shortcut_label || '回车直达')}]</div>
                  <div class="spotlight-item-path" style="color:var(--text-secondary);" title="${escapeHtml(h.detail)}">${escapeHtml(h.detail)}</div>
                </div>
              </div>
              <div class="spotlight-item-meta">
                <span class="badge-pill badge-safe" style="font-size:10px;">PRO 直达</span>
                <button class="btn btn-primary" style="padding:2px 8px; font-size:10px;" onclick="event.stopPropagation(); executeLauncherAction('${escapeHtml(h.action_type)}', '${escapePath(h.path)}')">执行</button>
              </div>
            </div>
          `;
        }

        const iconSvg = h.is_dir
          ? '<svg style="width:16px;height:16px;fill:#ffb900;" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>'
          : '<svg style="width:16px;height:16px;fill:#60cdff;" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>';
        
        let sizeBadge = '';
        if (h.is_dir) {
          sizeBadge = '<span class="badge-pill badge-neutral">目录</span>';
        } else if (h.is_recent) {
          sizeBadge = '<span class="badge-pill badge-neutral" style="font-size:10px;">历史</span>';
        } else {
          sizeBadge = `<span style="font-size:11px; color:var(--text-tertiary);">${formatBytes(h.size_bytes || 0)}</span>`;
        }

        const pathDisplay = h.is_recent ? `${h.detail} · ${h.path}` : h.path;

        return `
          <div class="spotlight-item ${isSelected ? 'selected' : ''}" onclick="selectAndExecuteSpotlightHit(${idx})">
            <div class="spotlight-item-left">
              ${iconSvg}
              <div style="display:flex; flex-direction:column; overflow:hidden;">
                <div class="spotlight-item-name">${escapeHtml(h.name)}</div>
                <div class="spotlight-item-path" title="${escapeHtml(pathDisplay)}">${escapeHtml(pathDisplay)}</div>
              </div>
            </div>
            <div class="spotlight-item-meta">
              ${sizeBadge}
              <button class="btn btn-secondary" style="padding:2px 6px; font-size:10px;" onclick="event.stopPropagation(); triggerQuickSwitch('${escapePath(h.path)}')">跳转</button>
              <button class="btn btn-primary" style="padding:2px 6px; font-size:10px;" onclick="event.stopPropagation(); openActionRunnerModal('${escapePath(h.path)}', '${escapeHtml(h.name)}')">动作</button>
            </div>
          </div>
        `;
      }).join('');

      const selEl = container.querySelector('.spotlight-item.selected');
      if (selEl) selEl.scrollIntoView({ block: 'nearest' });
    }

    function handleSpotlightKeydown(e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        closeSpotlight();
        return;
      }

      const input = document.getElementById('spotlightInput');
      const val = input ? input.value : '';

      // ArrowUp: 遍历历史搜索词 (当输入框为空或已处于历史翻看状态时) 或向上移动条目
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        if ((!val.trim() || queryHistoryIndex >= 0) && queryHistoryList.length > 0) {
          if (queryHistoryIndex === -1) {
            queryHistoryIndex = 0;
          } else {
            queryHistoryIndex = (queryHistoryIndex + 1) % queryHistoryList.length;
          }
          if (input) {
            input.value = queryHistoryList[queryHistoryIndex];
            executeSpotlightSearch(input.value);
          }
          return;
        }

        if (spotlightHits.length > 0) {
          spotlightSelectedIndex = (spotlightSelectedIndex - 1 + spotlightHits.length) % spotlightHits.length;
          renderSpotlightHits();
        }
        return;
      }

      // ArrowDown: 遍历较新历史搜索词 或向下移动条目
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (queryHistoryIndex >= 0 && queryHistoryList.length > 0) {
          if (queryHistoryIndex > 0) {
            queryHistoryIndex--;
            if (input) {
              input.value = queryHistoryList[queryHistoryIndex];
              executeSpotlightSearch(input.value);
            }
          } else {
            queryHistoryIndex = -1;
            if (input) {
              input.value = '';
              loadRecentSpotlightFiles();
            }
          }
          return;
        }

        if (spotlightHits.length > 0) {
          spotlightSelectedIndex = (spotlightSelectedIndex + 1) % spotlightHits.length;
          renderSpotlightHits();
        }
        return;
      }

      if (e.key === 'Enter') {
        e.preventDefault();
        if (spotlightHits[spotlightSelectedIndex]) {
          selectAndExecuteSpotlightHit(spotlightSelectedIndex);
        }
        return;
      }
      if (e.key === 'Tab') {
        e.preventDefault();
        if (spotlightHits[spotlightSelectedIndex]) {
          const item = spotlightHits[spotlightSelectedIndex];
          if (!item.is_launcher) {
            openActionRunnerModal(item.path, item.name);
          }
        }
        return;
      }
      if (e.ctrlKey && (e.key === 'g' || e.key === 'G')) {
        e.preventDefault();
        if (spotlightHits[spotlightSelectedIndex]) {
          triggerQuickSwitch(spotlightHits[spotlightSelectedIndex].path);
        }
        return;
      }
    }

    function selectAndExecuteSpotlightHit(idx) {
      const item = spotlightHits[idx];
      if (!item) return;
      if (item.is_launcher) {
        executeLauncherAction(item.action_type, item.path);
        closeSpotlight();
        return;
      }
      // 记录最近使用文件
      fetch('/api/history/record-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: item.path })
      }).catch(() => {});

      revealInExplorer(item.path);
      closeSpotlight();
    }

    // ==========================================
    // Listary Feature B: Quick Switch
    // ==========================================
    async function triggerQuickSwitch(targetPath) {
      if (!targetPath) {
        showToast('请选择待跳转的目标路径');
        return;
      }
      showToast('正在穿透前台对话框并注入路径...');
      try {
        const res = await fetch('/api/quick-switch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: targetPath })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`Quick Switch: ${data.message || '已成功跳转前台文件对话框'}`);
        } else {
          showToast(`Quick Switch 提示: ${data.error || '未检测到处于前台的 #32770 文件选择对话框'}`);
        }
      } catch (e) {
        showToast('Quick Switch 请求异常: ' + e.message);
      }
    }

    // ==========================================
    // ==========================================
    // Smart Action Hub (Contextual & Zero-Config)
    // ==========================================
    let currentActionTargetPath = '';
    let currentActionList = [];

    function switchActionHubTab(tab) {
      const tabActions = document.getElementById('tabActionViewItems');
      const tabTools = document.getElementById('tabActionViewTools');
      const boxActions = document.getElementById('actionRunnerItemsContainer');
      const boxTools = document.getElementById('actionRunnerToolsContainer');
      const hintText = document.getElementById('actionRunnerHintText');

      if (tab === 'tools') {
        if (tabActions) tabActions.classList.remove('active');
        if (tabTools) tabTools.classList.add('active');
        if (boxActions) boxActions.style.display = 'none';
        if (boxTools) {
          boxTools.style.display = 'flex';
          loadDetectedToolsView();
        }
        if (hintText) hintText.innerText = 'CleanFlow 已全自动侦测您的本地工具链，无需手动配置路径';
      } else {
        if (tabActions) tabActions.classList.add('active');
        if (tabTools) tabTools.classList.remove('active');
        if (boxActions) boxActions.style.display = 'flex';
        if (boxTools) boxTools.style.display = 'none';
        if (hintText) hintText.innerText = '按数字键 1-6 或点击卡片即刻执行';
      }
    }

    async function loadDetectedToolsView() {
      const container = document.getElementById('actionRunnerToolsContainer');
      if (!container) return;
      container.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-tertiary);">正在侦测系统已安装工具链...</div>';
      try {
        const res = await fetch('/api/actions/detected-tools');
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const tools = await res.json();

        const toolList = [
          { name: 'Visual Studio Code', key: tools.vscode, desc: tools.vscode ? '已侦测就绪，支持在工程目录和代码文件中一键呼出' : '未检测到默认安装路径' },
          { name: 'Windows Terminal (wt.exe)', key: tools.windows_terminal, desc: tools.windows_terminal ? '已就绪，秒开现代化多标签终端' : '未检测到，将回退至 PowerShell / CMD' },
          { name: 'Notepad++ 文本编辑器', key: tools.notepad_plus, desc: tools.notepad_plus ? '已侦测就绪，支持轻量级源码与配置高亮' : '未检测到' },
          { name: '7-Zip 压缩归档工具', key: tools.seven_zip, desc: tools.seven_zip ? '已侦测就绪，支持一键解压与归档' : '未检测到，将使用系统自带解压' },
          { name: 'Git 控制台与版本管理', key: tools.git, desc: tools.git ? '已侦测就绪，支持仓库快速初始化与定位' : '未检测到' },
        ];

        container.innerHTML = toolList.map(t => {
          const badge = t.key 
            ? '<span class="badge-pill badge-safe">已就绪 · 开箱即用</span>'
            : '<span class="badge-pill badge-neutral">未就绪</span>';
          const dotColor = t.key ? '#107c41' : '#8a8886';

          return `
            <div style="background:rgba(0,0,0,0.3); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:10px 14px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="width:8px; height:8px; border-radius:50%; background:${dotColor};"></span>
                <div>
                  <div style="font-size:12.5px; font-weight:600; color:#fff;">${escapeHtml(t.name)}</div>
                  <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">${escapeHtml(t.desc)}</div>
                </div>
              </div>
              <div>${badge}</div>
            </div>
          `;
        }).join('');
      } catch (e) {
        container.innerHTML = `<div style="padding:16px; color:var(--status-danger); text-align:center;">探测工具失败: ${escapeHtml(e.message)}</div>`;
      }
    }

    async function openActionRunnerModal(targetPath, targetName) {
      currentActionTargetPath = targetPath;
      currentActionList = [];
      const modal = document.getElementById('actionRunnerModal');
      const pathLabel = document.getElementById('actionRunnerTargetPath');
      const container = document.getElementById('actionRunnerItemsContainer');
      if (!modal || !container) return;

      switchActionHubTab('actions');
      if (pathLabel) pathLabel.innerText = targetPath;
      container.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-tertiary);">正在分析该项目适用的智能动作流水线...</div>';
      modal.classList.add('active');

      try {
        const res = await fetch('/api/actions/list?path=' + encodeURIComponent(targetPath));
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const actions = await res.json();
        currentActionList = actions || [];

        if (currentActionList.length === 0) {
          container.innerHTML = '<div style="padding:16px; color:var(--text-secondary); text-align:center;">暂无匹配动作</div>';
          return;
        }

        container.innerHTML = currentActionList.map((act, idx) => {
          let iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>';
          if (act.icon === 'code') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>';
          } else if (act.icon === 'terminal') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8h16v10zm-2-1h-6v-2h6v2zM7.5 17l-1.41-1.41L8.67 13l-2.58-2.59L7.5 9l4 4-4 4z"/></svg>';
          } else if (act.icon === 'switch') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M6.99 11L3 15l3.99 4v-3H14v-2H6.99v-3zM21 9l-3.99-4v3H10v2h7.01v3L21 9z"/></svg>';
          } else if (act.icon === 'copy') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>';
          } else if (act.icon === 'lock') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>';
          } else if (act.icon === 'hash') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.47-5.57 1.41-.24.13-.54.04-.68-.2-.13-.24-.04-.55.2-.68C7.82 2.52 9.86 2 12.01 2c2.13 0 3.99.47 6.03 1.52.25.13.34.43.21.67-.1.18-.28.28-.44.28zM3.5 9.72c-.1 0-.2-.03-.29-.09-.23-.16-.28-.47-.12-.7.99-1.4 2.25-2.5 3.75-3.27.25-.13.55-.03.67.22.12.24.03.54-.21.67-1.34.69-2.46 1.67-3.35 2.92-.1.16-.27.25-.45.25zM12 11c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2s2-.9 2-2v-8c0-1.1-.9-2-2-2z"/></svg>';
          } else if (act.icon === 'archive') {
            iconSvg = '<svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/></svg>';
          }

          let badgesHtml = '';
          if (act.is_recommended) {
            badgesHtml += '<span class="badge-pill badge-safe" style="font-size:10px; margin-right:4px;">推荐</span>';
          }
          if (act.is_pro) {
            badgesHtml += '<span class="badge-pill badge-neutral" style="font-size:10px; color:#60cdff; border-color:rgba(96,205,255,0.4);">PRO</span>';
          }

          const shortcutBadge = `<span class="spotlight-kbd" style="font-weight:700;">${escapeHtml(act.shortcut || String(idx + 1))}</span>`;
          const isHighlightBorder = act.is_recommended ? 'border-left: 3px solid #60cdff;' : '';

          return `
            <div class="action-card" style="${isHighlightBorder}" onclick="executeSelectedAction('${escapeHtml(act.id)}', '${escapePath(targetPath)}', ${act.is_pro})">
              <div class="action-card-left">
                <div class="action-card-icon" style="color:#60cdff;">
                  ${iconSvg}
                </div>
                <div>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <span class="action-card-title">${escapeHtml(act.title)}</span>
                    ${badgesHtml}
                  </div>
                  <div class="action-card-desc">${escapeHtml(act.description)}</div>
                </div>
              </div>
              <div>
                ${shortcutBadge}
              </div>
            </div>
          `;
        }).join('');
      } catch (e) {
        container.innerHTML = `<div style="padding:16px; color:var(--status-danger); text-align:center;">获取动作失败: ${escapeHtml(e.message)}</div>`;
      }
    }

    function closeActionRunnerModal() {
      const modal = document.getElementById('actionRunnerModal');
      if (modal) modal.classList.remove('active');
    }

    // Number key listener for instant action activation
    window.addEventListener('keydown', (e) => {
      const modal = document.getElementById('actionRunnerModal');
      if (!modal || !modal.classList.contains('active')) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        closeActionRunnerModal();
        return;
      }

      // Check number keys 1-9
      const num = parseInt(e.key, 10);
      if (!isNaN(num) && num >= 1 && num <= currentActionList.length) {
        e.preventDefault();
        const act = currentActionList[num - 1];
        if (act) {
          executeSelectedAction(act.id, currentActionTargetPath, act.is_pro);
        }
      }
    });

    async function executeSelectedAction(actionId, targetPath, isPro) {
      if (isPro && (!currentLicenseStatus || !currentLicenseStatus.is_pro)) {
        showToast('此动作为 PRO 专享特性，已为您展开授权面板，可立即免费开启 7 天体验！');
        openLicenseModal();
        return;
      }

      if (actionId === 'junction_migrate') {
        closeActionRunnerModal();
        startJunctionMigrateQuick(targetPath);
        return;
      }
      if (actionId === 'quick_switch') {
        closeActionRunnerModal();
        triggerQuickSwitch(targetPath);
        return;
      }

      showToast(`正在执行动作: ${actionId}...`);
      try {
        const res = await fetch('/api/actions/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action_id: actionId, target_path: targetPath })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`动作执行成功: ${data.message}`);
          closeActionRunnerModal();
        } else {
          showToast(`动作执行失败: ${data.error || '未知错误'}`);
        }
      } catch (e) {
        showToast('执行异常: ' + e.message);
      }
    }

    // ==========================================
    // Listary Feature D: Auto-Cleaner Daemon
    // ==========================================
    async function loadDaemonStatus() {
      const textEl = document.getElementById('daemonStatusText');
      const dotEl = document.getElementById('daemonStatusDot');
      if (!textEl || !dotEl) return;
      try {
        const res = await fetch('/api/daemon/status');
        if (!res.ok) return;
        const st = await res.json();
        if (st.running) {
          if (st.is_warning) {
            dotEl.style.background = '#d83b01';
            textEl.innerHTML = `<strong style="color:#ff8c00;">C:盘警告 (${st.free_gb.toFixed(1)}GB &lt; ${st.redline_gb}GB)</strong>`;
          } else {
            dotEl.style.background = '#107c41';
            textEl.innerText = `守护中 (C: 剩余 ${st.free_gb.toFixed(1)} GB)`;
          }
        } else {
          dotEl.style.background = '#8a8886';
          textEl.innerText = '守护进程未就绪';
        }
      } catch (e) {
        // Silently tolerate
      }
    }

    // Global Key Listener for Spotlight (双击 Ctrl / Alt+Space) & Search Focus (Ctrl+F)
    let lastCtrlPressTime = 0;
    window.addEventListener('keydown', (e) => {
      // 1. Listary signature gesture: Double-tap Ctrl (双击两下 Ctrl 键)
      if (e.key === 'Control' || e.code === 'ControlLeft' || e.code === 'ControlRight') {
        const now = Date.now();
        if (lastCtrlPressTime > 0 && (now - lastCtrlPressTime) <= 350) {
          lastCtrlPressTime = 0;
          const overlay = document.getElementById('spotlightOverlay');
          if (overlay && overlay.style.display !== 'none') {
            closeSpotlight();
          } else {
            openSpotlight();
          }
        } else {
          lastCtrlPressTime = now;
        }
        return;
      } else {
        lastCtrlPressTime = 0;
      }

      // 2. Alt+Space backup hotkey for Spotlight
      if (e.altKey && (e.code === 'Space' || e.key === ' ')) {
        e.preventDefault();
        const overlay = document.getElementById('spotlightOverlay');
        if (overlay && overlay.style.display !== 'none') {
          closeSpotlight();
        } else {
          openSpotlight();
        }
      }

      // 3. Ctrl+F for Search tab focusing
      if (e.ctrlKey && (e.code === 'KeyF' || e.key === 'f' || e.key === 'F')) {
        const inp = document.getElementById('searchInputField');
        if (inp && state.currentTab === 'search') {
          e.preventDefault();
          inp.focus();
          inp.select();
        }
      }
    });

    // ==========================================
    // CleanFlow Licensing & Pro Management
    // ==========================================
    let currentLicenseStatus = null;

    async function loadLicenseStatus() {
      try {
        const res = await fetch('/api/license/status');
        if (!res.ok) return;
        currentLicenseStatus = await res.json();
        updateLicenseUI();
      } catch (e) {
        // Silently tolerate
      }
    }

    function updateLicenseUI() {
      if (!currentLicenseStatus) return;
      const badge = document.getElementById('licenseStatusBadge');
      const tag = document.getElementById('licenseTierTag');
      const text = document.getElementById('licenseStatusText');
      if (badge && tag && text) {
        if (currentLicenseStatus.is_pro) {
          tag.innerText = currentLicenseStatus.tier === 'enterprise' ? 'ENT' : 'PRO';
          tag.style.background = '#60cdff';
          text.innerText = currentLicenseStatus.tier_display_name;
          badge.style.borderColor = 'rgba(96, 205, 255, 0.5)';
        } else {
          tag.innerText = 'FREE';
          tag.style.background = 'var(--text-tertiary)';
          text.innerText = '社区免费版';
          badge.style.borderColor = 'var(--stroke-card)';
        }
      }

      // Update Modal elements if open
      const modalTitle = document.getElementById('licModalTierTitle');
      const modalBadge = document.getElementById('licModalTierBadge');
      const modalDesc = document.getElementById('licModalDescription');
      const modalFp = document.getElementById('licModalFingerprint');
      const trialBanner = document.getElementById('licTrialBanner');

      if (modalTitle) modalTitle.innerText = currentLicenseStatus.tier_display_name;
      if (modalBadge) {
        modalBadge.innerText = currentLicenseStatus.is_pro ? 'PRO 尊享' : 'FREE 社区';
        modalBadge.className = currentLicenseStatus.is_pro ? 'badge-pill badge-safe' : 'badge-pill badge-neutral';
      }
      if (modalDesc) modalDesc.innerText = currentLicenseStatus.activation_message;
      if (modalFp) modalFp.innerText = '设备指纹: ' + (currentLicenseStatus.device_fingerprint || '----');
      if (trialBanner) {
        trialBanner.style.display = currentLicenseStatus.tier === 'community' ? 'flex' : 'none';
      }
    }

    function openLicenseModal() {
      const modal = document.getElementById('licenseModal');
      if (modal) modal.classList.add('active');
      loadLicenseStatus();
    }

    function closeLicenseModal() {
      const modal = document.getElementById('licenseModal');
      if (modal) modal.classList.remove('active');
    }

    async function startProTrialQuick() {
      try {
        const res = await fetch('/api/license/start-trial', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
          currentLicenseStatus = data.status;
          updateLicenseUI();
          showToast('PRO 7天全功能体验已成功开启！已解锁全部底层黑科技与工作流穿透！');
        } else {
          showToast(data.error || '开启体验失败');
        }
      } catch (e) {
        showToast('请求异常: ' + e.message);
      }
    }

    async function submitLicenseActivation() {
      const nameInp = document.getElementById('licInputName');
      const keyInp = document.getElementById('licInputKey');
      if (!keyInp || !keyInp.value.trim()) {
        showToast('请输入有效的激活码');
        return;
      }
      try {
        const res = await fetch('/api/license/activate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            licensee: nameInp ? nameInp.value.trim() : '',
            key: keyInp.value.trim()
          })
        });
        const data = await res.json();
        if (data.success) {
          currentLicenseStatus = data.status;
          updateLicenseUI();
          showToast('恭喜！授权激活成功，您已解锁 CleanFlow 终身 Pro 全部特权！');
          closeLicenseModal();
        } else {
          showToast(data.error || '激活失败，请检查激活码输入');
        }
      } catch (e) {
        showToast('激活请求网络异常: ' + e.message);
      }
    }

    // Init
    window.addEventListener('DOMContentLoaded', () => {
      refreshDisks();
      runScan();
      loadActiveJunctions();
      loadStartupItems();
      loadSystemMaintenance();
      loadInstalledApps();
      loadGiantFiles();
      loadDaemonStatus();
      loadLicenseStatus();
      setInterval(loadDaemonStatus, 15000);
      setInterval(loadLicenseStatus, 60000);
    });
  </script>
</body>
</html>
'''

if __name__ == "__main__":
    import os
    target_path = os.path.join(os.path.dirname(__file__), "src", "ui.html")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Generated: {target_path}")
