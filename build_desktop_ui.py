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
      padding: 24px 28px;
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
      grid-template-columns: repeat(3, 1fr);
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
      background-color: var(--bg-card);
      border: 1px solid var(--stroke-card-hover);
      border-radius: var(--radius-sm);
      padding: 8px 14px;
      font-size: 12px;
      color: #ffffff;
      box-shadow: var(--shadow-card);
      display: flex;
      align-items: center;
      gap: 8px;
      animation: toastIn 180ms var(--motion-spring);
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
      <span class="app-version-badge">v2.0</span>
    </div>

    <!-- Drive Switcher Pills -->
    <div class="titlebar-center" id="diskSelectorContainer">
      <!-- Injected via JS -->
    </div>

    <!-- Window Caption Controls -->
    <div class="titlebar-actions">
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
        <div class="nav-group-title">核心空间治理</div>
        <ul class="nav-list">
          <li class="nav-item active" onclick="switchTab('overview')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg></span>
              <span>空间概览</span>
            </div>
            <span class="nav-badge" id="badgeOverview">21.5 GB</span>
          </li>
          <li class="nav-item" onclick="switchTab('devcache')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg></span>
              <span>开发与编译包</span>
            </div>
            <span class="nav-badge" id="badgeDevCache">1.3 GB</span>
          </li>
          <li class="nav-item" onclick="switchTab('browser')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg></span>
              <span>浏览器深度专清</span>
            </div>
            <span class="nav-badge" id="badgeBrowser">856 MB</span>
          </li>
          <li class="nav-item" onclick="switchTab('registry')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-1 8h-3v3h-2v-3h-3v-2h3v-3h2v3h3v2z"/></svg></span>
              <span>注册表死链修复</span>
            </div>
            <span class="nav-badge" id="badgeRegistry">0</span>
          </li>
        </ul>

        <div class="nav-group-title" style="margin-top: 14px;">高级虚拟化与索引</div>
        <ul class="nav-list">
          <li class="nav-item" onclick="switchTab('giant')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
              <span>大文件全盘雷达</span>
            </div>
            <span class="nav-badge" id="badgeGiantFiles">89</span>
          </li>
          <li class="nav-item" onclick="switchTab('migration')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
              <span>目录无损搬家</span>
            </div>
            <span class="nav-badge">Junction</span>
          </li>
          <li class="nav-item" onclick="switchTab('vacuum')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 3C7.58 3 4 4.79 4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7c0-2.21-3.58-4-8-4zm0 2c3.87 0 6 1.5 6 2s-2.13 2-6 2-6-1.5-6-2 2.13-2 6-2zm0 14c-3.87 0-6-1.5-6-2v-1.85c1.47.78 3.61 1.25 6 1.25s4.53-.47 6-1.25V17c0 .5-2.13 2-6 2zm0-4c-3.87 0-6-1.5-6-2v-1.85c1.47.78 3.61 1.25 6 1.25s4.53-.47 6-1.25V13c0 .5-2.13 2-6 2z"/></svg></span>
              <span>数据库碎片收缩</span>
            </div>
            <span class="nav-badge">SQLite</span>
          </li>
          <li class="nav-item" onclick="switchTab('rules')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg></span>
              <span>自定义规则引擎</span>
            </div>
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

        <!-- 1. Consumer Overview Page -->
        <section class="workspace-pane active" id="pane-overview">
          
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
                    <span class="gauge-value" id="heroReclaimNum">21.5</span>
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
                <div class="hero-tags">
                  <span class="badge-pill badge-safe">
                    <span class="icon" style="width:12px; height:12px;"><svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                    100% 安全清理项已就绪
                  </span>
                  <span class="badge-pill badge-openwith">零后台常驻 · 本地原生引擎</span>
                </div>
              </div>
            </div>

            <div class="hero-right-actions">
              <button class="btn-hero-cta" onclick="executeCleanSelected()">
                <span class="icon" style="width:18px; height:18px;"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
                <span id="heroBtnCleanText">一键快速清理 (21.5 GB)</span>
              </button>
              <button class="btn btn-secondary" style="padding: 6px 14px;" onclick="runScan()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>重新深度体检</span>
              </button>
            </div>
          </div>

          <!-- 6 Consumer Feature Cards Grid -->
          <div class="consumer-cards-grid">
            <!-- Card 1: System Temp -->
            <div class="feature-card" onclick="openInspectorByCategory('system')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-cyan">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardSystemMetric">2.2 GB</div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">系统冗余与临时垃圾</div>
                <div class="card-desc">用户临时目录、Windows 补丁下载及崩溃转储文件</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">完全安全可清</span>
                <span class="card-action-link">查看详情 ></span>
              </div>
            </div>

            <!-- Card 2: Dev Cache -->
            <div class="feature-card" onclick="switchTab('devcache')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-green">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardDevMetric">1.3 GB</div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">现代开发与包管理器</div>
                <div class="card-desc">Unity、npm、Gradle、pnpm 离线依赖包与构建缓存</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">可安全回收</span>
                <span class="card-action-link">管理缓存 ></span>
              </div>
            </div>

            <!-- Card 3: Browser Cache -->
            <div class="feature-card" onclick="switchTab('browser')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-orange">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardBrowserMetric">856.7 MB</div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">主流浏览器深度专清</div>
                <div class="card-desc">Edge、Chrome 离线网络媒体与 JS/WASM 编译代码缓存</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-openwith">不影响登录态</span>
                <span class="card-action-link">立即专清 ></span>
              </div>
            </div>

            <!-- Card 4: Giant Files Radar -->
            <div class="feature-card" onclick="switchTab('giant')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-blue">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardGiantMetric">28.5 GB</div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">大文件全盘雷达</div>
                <div class="card-desc">排查 89 个超大沉淀文件（数据库、虚拟机盘与安装包）</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-openwith">深度探查</span>
                <span class="card-action-link">全盘排查 ></span>
              </div>
            </div>

            <!-- Card 5: Junction Migration -->
            <div class="feature-card" onclick="switchTab('migration')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-purple">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardJunctionMetric">+13.3 GB</div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">目录无损搬家 (Junction)</div>
                <div class="card-desc">Android 模拟器或微信数据无感搬迁至 D 盘，软件正常运行</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-junction">C 盘减负神器</span>
                <span class="card-action-link">一键搬家 ></span>
              </div>
            </div>

            <!-- Card 6: SQLite Vacuum -->
            <div class="feature-card" onclick="switchTab('vacuum')">
              <div class="feature-card-top">
                <div class="card-icon-box icon-box-cyan">
                  <svg style="width:20px; height:20px; fill:currentColor;" viewBox="0 0 24 24"><path d="M12 3C7.58 3 4 4.79 4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7c0-2.21-3.58-4-8-4zm0 2c3.87 0 6 1.5 6 2s-2.13 2-6 2-6-1.5-6-2 2.13-2 6-2zm0 14c-3.87 0-6-1.5-6-2v-1.85c1.47.78 3.61 1.25 6 1.25s4.53-.47 6-1.25V17c0 .5-2.13 2-6 2zm0-4c-3.87 0-6-1.5-6-2v-1.85c1.47.78 3.61 1.25 6 1.25s4.53-.47 6-1.25V13c0 .5-2.13 2-6 2z"/></svg>
                </div>
                <div class="feature-card-metric" id="cardVacuumMetric">4.0 GB</div>
              </div>
              <div class="feature-card-body">
                <div class="card-title">数据库碎片收缩 (VACUUM)</div>
                <div class="card-desc">Cursor 状态库物理压缩，清理 Freelist 空闲页无损减负</div>
              </div>
              <div class="feature-card-footer">
                <span class="badge-pill badge-safe">数据 100% 完整</span>
                <span class="card-action-link">执行收缩 ></span>
              </div>
            </div>
          </div>

          <!-- Quick Detailed Checklist Bar -->
          <div class="desktop-commandbar">
            <div class="commandbar-left">
              <div class="search-box">
                <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
                <input type="text" id="overviewSearchInput" placeholder="搜索体检项目或路径..." oninput="filterOverviewTable()">
              </div>
              <div class="filter-tabs">
                <div class="filter-tab active" onclick="setOverviewFilter('all', this)">全部项目</div>
                <div class="filter-tab" onclick="setOverviewFilter('safe', this)">安全推荐项</div>
                <div class="filter-tab" onclick="setOverviewFilter('dev', this)">开发工具</div>
                <div class="filter-tab" onclick="setOverviewFilter('browser', this)">浏览器</div>
              </div>
            </div>
            <span style="font-size:11.5px; color:var(--text-tertiary);" id="overviewCounter">就绪</span>
          </div>

          <!-- Clean Master DataGrid -->
          <div class="data-grid-container" style="max-height: 380px;">
            <table class="data-grid">
              <thead>
                <tr>
                  <th class="col-checkbox"><input type="checkbox" id="selectAllOverview" onchange="toggleSelectAllOverview(this.checked)" checked></th>
                  <th style="width: 180px;">清理项目</th>
                  <th>关联绝对物理路径</th>
                  <th style="width: 110px; text-align: right;">体积占用</th>
                  <th style="width: 90px; text-align: right;">文件数</th>
                  <th style="width: 90px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="overviewTableBody"></tbody>
            </table>
          </div>

        </section>

        <!-- 2. Dev Cache -->
        <section class="workspace-pane" id="pane-devcache">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>现代开发与包管理器缓存</h1>
              <p>释放 npm、pnpm、Unity、Gradle 等前端/后端/游戏引擎全局离线依赖包与编译缓存</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-primary" onclick="cleanCategoryItems('dev_cache')">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
                <span>清理开发缓存</span>
              </button>
            </div>
          </div>
          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th class="col-checkbox"><input type="checkbox" checked></th>
                  <th style="width: 220px;">技术栈 / 工具</th>
                  <th>缓存物理路径</th>
                  <th style="width: 110px; text-align: right;">占用体积</th>
                  <th style="width: 90px; text-align: right;">文件数</th>
                  <th style="width: 80px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="devCacheTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 3. Browser Cache -->
        <section class="workspace-pane" id="pane-browser">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>主流浏览器深度专清</h1>
              <p>安全清理 Microsoft Edge、Google Chrome 产生的离线网络多媒体与 JS/WASM 编译代码缓存，不影响历史记录与网站登录态</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-primary" onclick="cleanCategoryItems('browser_cache')">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
                <span>清理浏览器缓存</span>
              </button>
            </div>
          </div>
          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th class="col-checkbox"><input type="checkbox" checked></th>
                  <th style="width: 220px;">浏览器 / 缓存类型</th>
                  <th>磁盘物理路径</th>
                  <th style="width: 110px; text-align: right;">占用体积</th>
                  <th style="width: 90px; text-align: right;">文件数</th>
                  <th style="width: 80px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="browserTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 4. Registry Repair -->
        <section class="workspace-pane" id="pane-registry">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>注册表冗余与失效残留修复</h1>
              <p>排查已卸载历史软件的右键菜单残留、失效打开方式 (OpenWith) 及失效 MUICache，修复前自动生成可回滚 .reg 备份</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="loadRegistryIssues()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>重新扫描注册表</span>
              </button>
              <button class="btn btn-primary" onclick="executeCleanRegistry()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                <span id="btnCleanRegistryLabel">一键安全修复 (0 项)</span>
              </button>
            </div>
          </div>
          <div class="desktop-commandbar">
            <div class="commandbar-left">
              <div class="search-box">
                <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
                <input type="text" id="registrySearchInput" placeholder="按路径或软件名过滤..." oninput="renderRegistryTable()">
              </div>
              <div class="filter-tabs">
                <div class="filter-tab active" onclick="setRegistryFilter('all', this)">全部</div>
                <div class="filter-tab" onclick="setRegistryFilter('mui', this)">应用缓存 (MUICache)</div>
                <div class="filter-tab" onclick="setRegistryFilter('openwith', this)">右键打开方式 (OpenWith)</div>
                <div class="filter-tab" onclick="setRegistryFilter('uninst', this)">失效卸载项 (Uninstall)</div>
              </div>
            </div>
            <span style="font-size:11.5px; color:var(--text-tertiary);" id="registryCounter">准备就绪</span>
          </div>
          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th class="col-checkbox"><input type="checkbox" onchange="toggleSelectAllRegistry(this.checked)" checked></th>
                  <th style="width: 180px;">问题类型</th>
                  <th>失效引用的物理路径</th>
                  <th>注册表底层键路径</th>
                  <th style="width: 100px;">风险等级</th>
                  <th style="width: 80px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="registryTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 5. Giant Files Radar -->
        <section class="workspace-pane" id="pane-giant">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>大文件全盘雷达 (100MB+ 沉淀资产)</h1>
              <p>毫秒级排查深层隐藏的大型虚拟机盘、历史安装包、开发数据库与孤立压缩包</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="loadGiantFiles()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>刷新全盘雷达</span>
              </button>
            </div>
          </div>

          <!-- Type Distribution Segmented Bar -->
          <div style="background:var(--bg-card); border:1px solid var(--stroke-card); border-radius:var(--radius-md); padding:16px; display:flex; flex-direction:column; gap:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:12.5px; font-weight:600;">大文件资产类型占比与容量分层 (基于全盘检索)</span>
              <span style="font-size:12px; color:#60cdff; font-weight:600;" id="giantTotalSubtitle">总计 0 GB (0 个文件)</span>
            </div>
            <div style="height:10px; background:rgba(255,255,255,0.06); border-radius:var(--radius-pill); overflow:hidden; display:flex;" id="giantDistributionBar">
              <!-- Injected via JS -->
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:12px; font-size:11.5px;" id="giantLegendList">
              <!-- Injected via JS -->
            </div>
          </div>

          <div class="desktop-commandbar">
            <div class="commandbar-left">
              <div class="search-box">
                <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
                <input type="text" id="giantSearchInput" placeholder="按文件名或后缀过滤..." oninput="filterGiantTable()">
              </div>
              <div class="filter-tabs">
                <div class="filter-tab active" onclick="setGiantSizeFilter('all', this)">全部大小</div>
                <div class="filter-tab" onclick="setGiantSizeFilter('huge', this)">超大 (>1GB)</div>
                <div class="filter-tab" onclick="setGiantSizeFilter('large', this)">大文件 (500M-1G)</div>
                <div class="filter-tab" onclick="setGiantSizeFilter('med', this)">常规 (100M-500M)</div>
              </div>
            </div>
            <span style="font-size:11.5px; color:var(--text-tertiary);" id="giantCounter">加载中...</span>
          </div>

          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th style="width: 240px;">文件名称</th>
                  <th>磁盘绝对路径</th>
                  <th style="width: 100px;">资产分类</th>
                  <th style="width: 110px; text-align: right;">文件体积</th>
                  <th style="width: 80px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="giantTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 6. Junction Migration -->
        <section class="workspace-pane" id="pane-migration">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>目录无损搬家 (Junction 虚拟化)</h1>
              <p>将庞大资产搬迁至 D 盘或其它大容量驱动器，原位创建 NTFS Junction，软件无感照常运行</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="loadActiveJunctions()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>刷新活动软链接</span>
              </button>
            </div>
          </div>

          <!-- Dual Drive Forecast Card -->
          <div style="background:var(--bg-card); border:1px solid var(--stroke-card); border-radius:var(--radius-md); padding:18px; display:flex; flex-direction:column; gap:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:13px; font-weight:600;">空间无损搬迁效益预测 (NTFS Junction 重定向)</span>
              <span class="badge-pill badge-safe">100% 透明无损 · 原位创建虚拟联接点</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
              <div style="background:rgba(0,0,0,0.2); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                  <span style="color:var(--text-secondary);">源磁盘 (C: 盘) 释放预测</span>
                  <span style="color:var(--status-safe); font-weight:600;">预计释放 +13.3 GB</span>
                </div>
                <div style="height:8px; background:rgba(255,255,255,0.08); border-radius:4px; overflow:hidden; display:flex;">
                  <div style="width:78%; background:#0078d4;"></div>
                  <div style="width:7%; background:#00c7ff;"></div>
                  <div style="width:15%; background:transparent;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-tertiary); margin-top:6px;">
                  <span>当前可用 33.0 GB</span>
                  <span style="color:#60cdff;">搬迁后预计提升至 46.3 GB</span>
                </div>
              </div>
              <div style="background:rgba(0,0,0,0.2); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                  <span style="color:var(--text-secondary);">目标磁盘 (D: 盘) 承载状态</span>
                  <span style="color:#60cdff; font-weight:600;">93.1 GB 充足容量</span>
                </div>
                <div style="height:8px; background:rgba(255,255,255,0.08); border-radius:4px; overflow:hidden; display:flex;">
                  <div style="width:75%; background:var(--status-purple);"></div>
                  <div style="width:25%; background:transparent;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-tertiary); margin-top:6px;">
                  <span>本地高速 SSD</span>
                  <span>跨盘读写完全透明</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Custom Migration Input Box -->
          <div style="background:var(--bg-card); border:1px solid var(--stroke-card); border-radius:var(--radius-md); padding:16px; display:flex; flex-direction:column; gap:12px;">
            <div style="font-weight:600; font-size:12.5px; color:var(--text-primary);">自定义任意目录一键搬家</div>
            <div style="display:flex; gap:10px; align-items:center;">
              <input type="text" id="customMigrateSource" placeholder="输入或粘贴需要搬迁的 C 盘目录绝对路径 (如 C:\Users\EDY\.android\avd)..." style="flex:1; background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:7px 12px; color:#fff; font-size:12px; outline:none; font-family:var(--font-mono);">
              <select id="customMigrateTargetDrive" style="background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:7px 12px; color:#fff; font-size:12px; outline:none;">
                <option value="D:">D 盘 (本地大容量磁盘)</option>
                <option value="E:">E 盘</option>
              </select>
              <button class="btn btn-secondary" onclick="analyzeCustomMigrationPath()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg></span>
                <span>分析体积与进程占用</span>
              </button>
              <button class="btn btn-primary" onclick="executeCustomMigration()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
                <span>立即安全迁移并创建 Junction</span>
              </button>
            </div>
          </div>

          <div style="font-weight:600; font-size:13px; color:var(--text-primary); margin-top:4px;">当前活动的 Junction 目录联接 (已搬迁项)</div>
          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th style="width: 320px;">原始 C 盘虚拟路径</th>
                  <th>实际物理存储位置</th>
                  <th style="width: 140px;">创建时间</th>
                  <th style="width: 140px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="activeJunctionsTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 7. SQLite Vacuum -->
        <section class="workspace-pane" id="pane-vacuum">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>SQLite 数据库碎片无损收缩</h1>
              <p>对长期高频读写的 SQLite 数据库执行 VACUUM 命令，释放游离的 Freelist 闲置数据页</p>
            </div>
          </div>
          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th style="width: 220px;">数据库名称与用途</th>
                  <th>底层数据库路径</th>
                  <th style="width: 110px; text-align: right;">当前物理体积</th>
                  <th style="width: 120px; text-align: center;">碎片释放潜能</th>
                  <th style="width: 110px; text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="vacuumTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 8. Custom Rules -->
        <section class="workspace-pane" id="pane-rules">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>自定义规则引擎</h1>
              <p>配置用户专属的项目构建缓存与特定临时目录匹配规则</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="renderCustomRulesTable()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>刷新规则库</span>
              </button>
            </div>
          </div>

          <div style="background:var(--bg-card); border:1px solid var(--stroke-card); border-radius:var(--radius-md); padding:16px; display:flex; flex-direction:column; gap:12px;">
            <div style="font-weight:600; font-size:12.5px; color:var(--text-primary);">创建专属巡检清理规则</div>
            <div style="display:flex; gap:12px; align-items:flex-end;">
              <div style="flex:1;">
                <label style="font-size:11.5px; color:var(--text-secondary); display:block; margin-bottom:5px;">规则名称</label>
                <input type="text" id="ruleNameInput" placeholder="例如: Webpack dist 构建产物" style="width:100%; background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none;">
              </div>
              <div style="flex:2;">
                <label style="font-size:11.5px; color:var(--text-secondary); display:block; margin-bottom:5px;">绝对路径模式 (支持 %LOCALAPPDATA% 等环境变量与通配符)</label>
                <input type="text" id="rulePatternInput" placeholder="例如: %LOCALAPPDATA%\MyTool\cache\*" style="width:100%; background:var(--fill-subtle); border:1px solid var(--stroke-card); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none; font-family:var(--font-mono);">
              </div>
              <button class="btn btn-primary" style="height:32px; padding:0 14px;" onclick="submitCustomRule()">
                <span>保存规则</span>
              </button>
            </div>
          </div>

          <div class="data-grid-container" style="flex: 1;">
            <table class="data-grid">
              <thead>
                <tr>
                  <th style="width: 140px;">治理分类</th>
                  <th style="width: 220px;">规则名称</th>
                  <th>路径匹配模式 / 变量</th>
                  <th style="width: 120px; text-align: center;">装载状态</th>
                </tr>
              </thead>
              <tbody id="customRulesTableBody"></tbody>
            </table>
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
      <span>Rust 原生内核 v0.1.0 · <span style="color:var(--status-safe);">零后台常驻</span></span>
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

    // Tab Switching
    function switchTab(tabId) {
      state.currentTab = tabId;
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.workspace-pane').forEach(el => el.classList.remove('active'));

      const pane = document.getElementById(`pane-${tabId}`);
      if (pane) pane.classList.add('active');

      const navMap = {
        'overview': 0, 'devcache': 1, 'browser': 2, 'registry': 3,
        'giant': 4, 'migration': 5, 'vacuum': 6, 'rules': 7
      };
      const items = document.querySelectorAll('.nav-item');
      if (items[navMap[tabId]]) items[navMap[tabId]].classList.add('active');

      if (tabId === 'giant' && state.giantFiles.length === 0) loadGiantFiles();
      if (tabId === 'registry' && state.registryIssues.length === 0) loadRegistryIssues();
      if (tabId === 'migration') loadActiveJunctions();
      if (tabId === 'rules') renderCustomRulesTable();
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
        const inp = document.querySelector('.workspace-pane.active input[type="text"]');
        if (inp) inp.focus();
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
        document.getElementById('heroReclaimNum').innerText = totalGbStr;
        document.getElementById('badgeOverview').innerText = `${totalGbStr} GB`;
        document.getElementById('heroBtnCleanText').innerText = `一键快速清理 (${totalGbStr} GB)`;

        // Update Gauge Circle stroke-dashoffset
        const circle = document.getElementById('heroGaugeCircle');
        const offset = Math.max(80, 440 - Math.min(360, (totalReclaimable / (40 * 1024**3)) * 360));
        circle.style.strokeDashoffset = offset;

        // Update Card Metrics
        const sysCat = state.scanReport.categories.find(c => c.id === 'system');
        if (sysCat) document.getElementById('cardSystemMetric').innerHTML = formatMetricHtml(sysCat.total_size_bytes);

        const devCat = state.scanReport.categories.find(c => c.id === 'dev_cache');
        if (devCat) {
          document.getElementById('cardDevMetric').innerHTML = formatMetricHtml(devCat.total_size_bytes);
          document.getElementById('badgeDevCache').innerText = formatBytes(devCat.total_size_bytes);
        }

        const bCat = state.scanReport.categories.find(c => c.id === 'browser_cache');
        if (bCat) {
          document.getElementById('cardBrowserMetric').innerHTML = formatMetricHtml(bCat.total_size_bytes);
          document.getElementById('badgeBrowser').innerText = formatBytes(bCat.total_size_bytes);
        }

        const vacCat = state.scanReport.categories.find(c => c.id === 'sqlite_optimize' || c.id === 'db_vacuum');
        if (vacCat) document.getElementById('cardVacuumMetric').innerHTML = formatMetricHtml(vacCat.total_size_bytes);

        renderOverviewTable();
        renderDevCacheTable();
        renderBrowserTable();
        renderVacuumTable();
        renderCustomRulesTable();

        document.getElementById('sbProgress').innerText = '体检完成';
        updateSelectionStatus();
        showToast('空间体检完成，已识别可释放空间');
      } catch (e) {
        console.error('Scan error', e);
        showToast('体检失败: ' + e.message);
      }
    }

    function renderOverviewTable() {
      const tbody = document.getElementById('overviewTableBody');
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

      document.getElementById('overviewCounter').innerText = `已检出 ${renderedCount} 处清理项`;
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
      document.getElementById('sbSelection').innerText = `已选 ${state.selectedPaths.size} 项 (${formatBytes(selBytes)})`;
      document.getElementById('heroBtnCleanText').innerText = `一键快速清理 (${formatBytes(selBytes)})`;
    }

    // Dev Cache Table
    function renderDevCacheTable() {
      const tbody = document.getElementById('devCacheTableBody');
      tbody.innerHTML = '';
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === 'dev_cache');
      if (!cat) return;

      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          if (mp.size_bytes === 0) return;
          const tr = document.createElement('tr');
          tr.setAttribute('data-path', mp.path);
          tr.setAttribute('data-name', r.name);
          tr.setAttribute('data-size', mp.size_bytes);
          tr.setAttribute('data-cat', '开发缓存');
          tr.onclick = (e) => {
            if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
              document.querySelectorAll('.data-grid tbody tr').forEach(row => row.classList.remove('selected'));
              tr.classList.add('selected');
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: '开发缓存' });
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

    // Browser Cache Table
    function renderBrowserTable() {
      const tbody = document.getElementById('browserTableBody');
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
      document.getElementById('registryCounter').innerText = '扫描中...';
      try {
        const res = await fetch('/api/registry/scan');
        state.registryIssues = await res.json();
        state.selectedRegistryIds = new Set(state.registryIssues.map(i => i.id));
        document.getElementById('badgeRegistry').innerText = state.registryIssues.length;
        renderRegistryTable();
        showToast(`排查出 ${state.registryIssues.length} 处失效注册表条目`);
      } catch (e) {
        showToast('注册表扫描失败: ' + e.message);
      }
    }

    function renderRegistryTable() {
      const tbody = document.getElementById('registryTableBody');
      tbody.innerHTML = '';
      const q = (document.getElementById('registrySearchInput')?.value || '').toLowerCase();
      const filtered = state.registryIssues.filter(item => {
        if (state.registryFilterCategory === 'mui' && !item.category.includes('MUICache')) return false;
        if (state.registryFilterCategory === 'openwith' && !item.category.includes('OpenWith')) return false;
        if (state.registryFilterCategory === 'uninst' && !item.category.includes('Uninstall')) return false;
        if (q) return item.invalid_path.toLowerCase().includes(q) || item.category.toLowerCase().includes(q) || item.root_key.toLowerCase().includes(q);
        return true;
      });

      document.getElementById('registryCounter').innerText = `发现 ${filtered.length} 处冗余项目`;
      document.getElementById('btnCleanRegistryLabel').innerText = `一键安全修复 (${state.selectedRegistryIds.size} 项)`;

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
      document.getElementById('giantCounter').innerText = '排查中...';
      try {
        const res = await fetch('/api/giant-files');
        state.giantFiles = await res.json();
        document.getElementById('badgeGiantFiles').innerText = state.giantFiles.length;
        document.getElementById('cardGiantMetric').innerText = `${(state.giantFiles.reduce((acc, f) => acc + f.size_bytes, 0) / (1024**3)).toFixed(1)} GB`;
        renderGiantDistribution();
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

      document.getElementById('giantTotalSubtitle').innerText = `总计 ${formatBytes(totalBytes)} (${state.giantFiles.length} 个文件)`;

      const bar = document.getElementById('giantDistributionBar');
      bar.innerHTML = '';
      const legend = document.getElementById('giantLegendList');
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
      const tbody = document.getElementById('giantTableBody');
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

      document.getElementById('giantCounter').innerText = `已排查出 ${filtered.length} 个大型资产`;

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
        const catZh = f.category === 'Database' ? '数据库' : f.category === 'VirtualDisk' ? '虚拟机' : f.category === 'Installer' ? '安装包' : f.category === 'Archive' ? '压缩包' : '大资产';
        const badgeStyle = f.category === 'Database' ? 'badge-safe' : f.category === 'VirtualDisk' ? 'badge-junction' : f.category === 'Installer' ? 'badge-warn' : 'badge-openwith';

        tr.innerHTML = `
          <td style="font-weight:600;"><span class="path-text" title="${escapeHtml(f.name)}" style="color:#ffffff;">${escapeHtml(f.name)}</span></td>
          <td><span class="path-text" title="${escapeHtml(f.path)}">${escapeHtml(f.path)}</span></td>
          <td><span class="badge-pill ${badgeStyle}">${escapeHtml(catZh)}</span></td>
          <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(f.size_bytes)}</td>
          <td style="text-align: center;">
            <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(f.path)}')">定位</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Junction Migration
    async function loadActiveJunctions() {
      try {
        const res = await fetch('/api/junctions');
        const list = await res.json();
        const tbody = document.getElementById('activeJunctionsTableBody');
        tbody.innerHTML = '';
        if (list.length === 0) {
          tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 24px; color: var(--text-tertiary);">当前尚未创建任何活动软联接</td></tr>`;
          return;
        }
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
      } catch (e) {
        console.error('Failed to load junctions', e);
      }
    }

    async function analyzeCustomMigrationPath() {
      const src = document.getElementById('customMigrateSource').value.trim();
      if (!src) {
        showToast('请输入需要分析的目录路径');
        return;
      }
      showToast('正在分析该路径体积与排查占用锁...');
      try {
        const res = await fetch('/api/check-path', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: src })
        });
        const data = await res.json();
        if (data.exists) {
          inspectItem({
            name: src.split('\\').pop() || '目录资产',
            path: src,
            size_bytes: data.size_bytes,
            file_count: data.file_count,
            category: '待搬迁目录'
          });
          showToast(`已分析: 体积 ${formatBytes(data.size_bytes)}，包含 ${data.file_count} 个文件`);
        } else {
          showToast('分析失败: ' + (data.error || '路径不存在'));
        }
      } catch (e) {
        showToast('请求异常: ' + e.message);
      }
    }

    function executeCustomMigration() {
      const src = document.getElementById('customMigrateSource').value.trim();
      const targetDrive = document.getElementById('customMigrateTargetDrive').value;
      if (!src) {
        showToast('请填写需要搬迁的源目录绝对路径');
        return;
      }
      openConfirmModal('Junction 虚拟化搬家确认', `即将把目录 <br><b>${escapeHtml(src)}</b><br> 完整搬迁至 <b>${targetDrive}</b> 驱动器，并在原位自动创建 NTFS Junction。<br><br>所有软件、环境变量均不受影响，完全无感照常运行。`, async () => {
        closeConfirmModal();
        showToast('正在执行跨驱动器搬家与虚拟化...');
        try {
          const res = await fetch('/api/migrate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_path: src, target_drive: targetDrive })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`搬迁成功！已在原位建立 Junction，释放 ${formatBytes(data.bytes_freed || 0)}`);
            document.getElementById('customMigrateSource').value = '';
            loadActiveJunctions();
            refreshDisks();
            runScan();
          } else {
            showToast('搬迁失败: ' + (data.error || '未知错误'));
          }
        } catch (e) {
          showToast('搬迁异常: ' + e.message);
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

    // Init
    window.addEventListener('DOMContentLoaded', () => {
      refreshDisks();
      runScan();
      loadActiveJunctions();
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
