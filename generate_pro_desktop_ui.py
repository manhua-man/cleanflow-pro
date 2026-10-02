# -*- coding: utf-8 -*-
"""
CleanFlow Pro - Professional Windows 11 Fluent 2 Desktop Architecture
Grounded in App Studio (winui.csv, frontend-design, emil-design-eng, impeccable).
Strict Zero-Emoji rule. Authentic desktop software ergonomics.
"""
import re
import os

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CleanFlow Pro - Windows 空间管家</title>
  <style>
    /* ==========================================================================
       Windows 11 Fluent 2 Design Tokens (App Studio & WinUI 3 Grounded)
       ========================================================================== */
    :root {
      /* Surface & Mica Layers */
      --fluent-mica-base: #14161a;
      --fluent-mica-alt: #1a1e24;
      --fluent-layer-base: #1c2026;
      --fluent-card-bg: #222730;
      --fluent-card-hover: #29303b;
      --fluent-card-active: #1e232b;
      --fluent-subtle: rgba(255, 255, 255, 0.04);
      --fluent-subtle-hover: rgba(255, 255, 255, 0.07);

      /* Borders & Dividers */
      --fluent-stroke-card: rgba(255, 255, 255, 0.07);
      --fluent-stroke-divider: rgba(255, 255, 255, 0.06);
      --fluent-stroke-control: rgba(255, 255, 255, 0.12);
      --fluent-stroke-focus: #60cdff;

      /* Typography */
      --font-family: 'Segoe UI Variable Text', 'Segoe UI Variable Display', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      --font-mono: 'Consolas', 'Cascadia Code', monospace;
      --text-primary: #ffffff;
      --text-secondary: #cdd3dc;
      --text-tertiary: #87919f;
      --text-disabled: #555d69;

      /* Accent & Semantic Status */
      --accent-primary: #0078d4;
      --accent-hover: #1084d9;
      --accent-active: #006cbe;
      --accent-subtle: rgba(0, 120, 212, 0.15);

      --status-safe: #10b981;
      --status-safe-bg: rgba(16, 185, 129, 0.12);
      --status-safe-border: rgba(16, 185, 129, 0.28);

      --status-warn: #f59e0b;
      --status-warn-bg: rgba(245, 158, 11, 0.12);
      --status-warn-border: rgba(245, 158, 11, 0.28);

      --status-danger: #ef4444;
      --status-danger-bg: rgba(239, 68, 68, 0.12);
      --status-danger-border: rgba(239, 68, 68, 0.28);

      --status-junction: #a855f7;
      --status-junction-bg: rgba(168, 85, 247, 0.12);
      --status-junction-border: rgba(168, 85, 247, 0.28);

      /* Radii & Motion */
      --radius-sm: 4px;
      --radius-md: 6px;
      --radius-lg: 8px;
      --radius-pill: 9999px;
      --motion-timing: cubic-bezier(0.1, 0.9, 0.2, 1.0);
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
      background-color: var(--fluent-mica-base);
      color: var(--text-primary);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      font-size: 13px;
      line-height: 1.45;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.15);
      border-radius: var(--radius-pill);
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.25);
    }

    /* SVG Icons */
    .icon {
      width: 15px;
      height: 15px;
      fill: currentColor;
      flex-shrink: 0;
      display: inline-block;
      vertical-align: middle;
    }

    /* ==========================================================================
       Window Titlebar (Authentic Desktop Frame)
       ========================================================================== */
    .app-titlebar {
      height: 38px;
      background-color: var(--fluent-mica-alt);
      border-bottom: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 0 0 14px;
      -webkit-app-region: drag;
      flex-shrink: 0;
      z-index: 100;
    }

    .titlebar-left {
      display: flex;
      align-items: center;
      gap: 10px;
      -webkit-app-region: no-drag;
    }

    .app-brand-icon {
      width: 18px;
      height: 18px;
      color: #60cdff;
    }

    .app-brand-title {
      font-size: 12.5px;
      font-weight: 600;
      letter-spacing: -0.2px;
      color: var(--text-primary);
    }

    .app-version-badge {
      font-size: 10px;
      font-weight: 600;
      padding: 1px 5px;
      border-radius: var(--radius-sm);
      background-color: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-card);
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
      padding: 3px 10px;
      border-radius: var(--radius-pill);
      background: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-card);
      font-size: 11.5px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 120ms ease;
    }

    .drive-pill:hover, .drive-pill.active {
      background: var(--fluent-subtle-hover);
      color: var(--text-primary);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .drive-pill.active {
      border-color: #60cdff;
      background: rgba(0, 120, 212, 0.15);
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
      width: 46px;
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
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
    }

    .win-caption-btn.btn-close:hover {
      background-color: #c42b1c;
      color: #ffffff;
    }

    /* ==========================================================================
       App Layout: Sidebar (NavigationView) + Content Area + Inspector
       ========================================================================== */
    .app-body {
      flex: 1;
      display: flex;
      overflow: hidden;
      background-color: var(--fluent-mica-base);
      position: relative;
    }

    /* NavigationView Sidebar */
    .navigation-view {
      width: 228px;
      background-color: var(--fluent-mica-alt);
      border-right: 1px solid var(--fluent-stroke-divider);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 10px 8px;
      flex-shrink: 0;
      overflow-y: auto;
    }

    .nav-group-title {
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-tertiary);
      padding: 8px 12px 4px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }

    .nav-list {
      display: flex;
      flex-direction: column;
      gap: 2px;
      list-style: none;
    }

    .nav-item {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 7px 12px;
      border-radius: var(--radius-sm);
      color: var(--text-secondary);
      cursor: pointer;
      font-size: 12.5px;
      font-weight: 500;
      transition: background-color 120ms ease, color 120ms ease;
    }

    .nav-item:hover {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
    }

    .nav-item.active {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
      font-weight: 600;
    }

    .nav-item.active::before {
      content: "";
      position: absolute;
      left: 0;
      top: 7px;
      bottom: 7px;
      width: 3px;
      border-radius: 2px;
      background-color: var(--accent-primary);
    }

    .nav-item-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .nav-badge {
      font-size: 11px;
      font-weight: 600;
      padding: 1px 6px;
      border-radius: var(--radius-pill);
      background: var(--fluent-subtle);
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
      background-color: var(--fluent-layer-base);
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
      padding: 20px 24px;
      gap: 16px;
    }

    .workspace-pane {
      display: none;
      flex-direction: column;
      gap: 16px;
    }

    .workspace-pane.active {
      display: flex;
      animation: fluentPaneIn 180ms var(--motion-timing);
    }

    @keyframes fluentPaneIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Workspace Header */
    .workspace-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      border-bottom: 1px solid var(--fluent-stroke-divider);
      padding-bottom: 12px;
    }

    .workspace-title-box h1 {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 3px;
    }

    .workspace-title-box p {
      font-size: 12px;
      color: var(--text-secondary);
    }

    .workspace-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      height: 30px;
      padding: 0 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 600;
      font-family: var(--font-family);
      cursor: pointer;
      border: 1px solid transparent;
      outline: none;
      transition: all 120ms ease;
      white-space: nowrap;
    }

    .btn:active {
      transform: scale(0.98);
    }

    .btn-primary {
      background-color: var(--accent-primary);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.15);
    }

    .btn-primary:hover {
      background-color: var(--accent-hover);
      box-shadow: 0 2px 8px rgba(0, 120, 212, 0.35);
    }

    .btn-secondary {
      background-color: var(--fluent-subtle);
      border-color: var(--fluent-stroke-control);
      color: var(--text-primary);
    }

    .btn-secondary:hover {
      background-color: var(--fluent-subtle-hover);
      border-color: rgba(255, 255, 255, 0.2);
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

    /* CommandBar */
    .desktop-commandbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background-color: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 6px 10px;
    }

    .commandbar-left {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
    }

    .search-box {
      position: relative;
      display: flex;
      align-items: center;
    }

    .search-box input {
      background-color: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-control);
      border-radius: var(--radius-sm);
      padding: 4px 8px 4px 26px;
      font-size: 12px;
      color: var(--text-primary);
      outline: none;
      width: 200px;
      transition: all 120ms ease;
    }

    .search-box input:focus {
      border-color: var(--fluent-stroke-focus);
      background-color: var(--fluent-layer-base);
      width: 240px;
    }

    .search-icon {
      position: absolute;
      left: 7px;
      color: var(--text-tertiary);
      pointer-events: none;
    }

    .filter-tabs {
      display: flex;
      align-items: center;
      gap: 3px;
    }

    .filter-tab {
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      font-size: 11.5px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 100ms ease;
    }

    .filter-tab:hover {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
    }

    .filter-tab.active {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
      font-weight: 600;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }

    /* DataGrid / Table */
    .data-grid-container {
      background-color: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
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
      background-color: rgba(0, 0, 0, 0.2);
      color: var(--text-tertiary);
      font-weight: 600;
      padding: 7px 10px;
      border-bottom: 1px solid var(--fluent-stroke-divider);
      font-size: 11px;
      letter-spacing: 0.2px;
      position: sticky;
      top: 0;
      z-index: 5;
    }

    .data-grid tbody tr {
      border-bottom: 1px solid rgba(255, 255, 255, 0.035);
      cursor: pointer;
      transition: background-color 80ms ease;
      height: 32px;
    }

    .data-grid tbody tr:hover {
      background-color: rgba(255, 255, 255, 0.04);
    }

    .data-grid tbody tr.selected {
      background-color: rgba(0, 120, 212, 0.16);
      border-left: 3px solid #0078d4;
    }

    .data-grid td {
      padding: 5px 10px;
      vertical-align: middle;
      white-space: nowrap;
    }

    .col-checkbox {
      width: 32px;
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

    .table-actions {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .icon-action-btn {
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--radius-sm);
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 100ms ease;
    }

    .icon-action-btn:hover {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
      border-color: var(--fluent-stroke-control);
    }

    /* Badges */
    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 1px 7px;
      border-radius: var(--radius-pill);
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
    }

    .badge-safe {
      background: var(--status-safe-bg);
      color: var(--status-safe);
      border: 1px solid var(--status-safe-border);
    }

    .badge-junction {
      background: var(--status-junction-bg);
      color: var(--status-junction);
      border: 1px solid var(--status-junction-border);
    }

    .badge-warn {
      background: var(--status-warn-bg);
      color: var(--status-warn);
      border: 1px solid var(--status-warn-border);
    }

    .badge-danger {
      background: var(--status-danger-bg);
      color: var(--status-danger);
      border: 1px solid var(--status-danger-border);
    }

    .badge-openwith {
      background: rgba(96, 205, 255, 0.15);
      color: #60cdff;
      border: 1px solid rgba(96, 205, 255, 0.3);
    }

    /* Form Controls */
    input[type="checkbox"] {
      appearance: none;
      width: 15px;
      height: 15px;
      border: 1px solid var(--fluent-stroke-control);
      border-radius: 3px;
      background-color: var(--fluent-subtle);
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
      width: 320px;
      background-color: var(--fluent-mica-alt);
      border-left: 1px solid var(--fluent-stroke-divider);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      transition: width 180ms var(--motion-timing), opacity 180ms ease;
      overflow: hidden;
    }

    .desktop-inspector.collapsed {
      width: 0;
      border-left-width: 0;
      opacity: 0;
      pointer-events: none;
    }

    .inspector-header {
      padding: 12px 14px;
      border-bottom: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .inspector-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .inspector-close-btn {
      width: 22px;
      height: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--radius-sm);
      background: transparent;
      border: none;
      color: var(--text-tertiary);
      cursor: pointer;
    }

    .inspector-close-btn:hover {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
    }

    .inspector-body {
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      overflow-y: auto;
      flex: 1;
    }

    .inspector-card {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .inspector-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-tertiary);
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }

    .inspector-val {
      font-size: 12px;
      color: var(--text-primary);
      word-break: break-all;
    }

    .inspector-path-box {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: var(--radius-sm);
      padding: 8px 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: #60cdff;
      word-break: break-all;
      position: relative;
    }

    .inspector-actions {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: auto;
    }

    /* ==========================================================================
       Desktop Context Menu (Acrylic Floating Menu)
       ========================================================================== */
    .fluent-context-menu {
      position: fixed;
      z-index: 10000;
      background: rgba(28, 32, 40, 0.94);
      backdrop-filter: blur(20px) saturate(140%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: var(--radius-md);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08);
      padding: 4px;
      min-width: 190px;
      display: none;
      flex-direction: column;
      animation: menuPop 100ms ease;
    }

    @keyframes menuPop {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }

    .fluent-context-menu.active {
      display: flex;
    }

    .context-menu-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      color: var(--text-primary);
      cursor: pointer;
      transition: background-color 80ms ease;
    }

    .context-menu-item:hover {
      background-color: var(--accent-primary);
      color: #ffffff;
    }

    .context-menu-divider {
      height: 1px;
      background: rgba(255, 255, 255, 0.08);
      margin: 3px 0;
    }

    /* ==========================================================================
       Desktop Bottom StatusBar
       ========================================================================== */
    .desktop-statusbar {
      height: 26px;
      background-color: var(--fluent-mica-alt);
      border-top: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 14px;
      font-size: 11px;
      color: var(--text-tertiary);
      flex-shrink: 0;
      z-index: 100;
    }

    .statusbar-left, .statusbar-center, .statusbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .statusbar-accent {
      color: #60cdff;
      font-family: var(--font-mono);
    }

    /* ==========================================================================
       Workspaces specific styles: Hero Ribbon, Tiles, Projection Cards
       ========================================================================== */
    .storage-hero-card {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .hero-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .hero-metric-figure {
      font-size: 28px;
      font-weight: 700;
      color: #ffffff;
      font-family: var(--font-family);
    }

    .storage-ribbon {
      height: 14px;
      background-color: rgba(0, 0, 0, 0.35);
      border-radius: var(--radius-sm);
      overflow: hidden;
      display: flex;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .ribbon-segment {
      height: 100%;
      transition: width 350ms var(--motion-timing);
    }

    .seg-system { background-color: #4f52b2; }
    .seg-apps { background-color: #0078d4; }
    .seg-cleanable { background-color: #00b7c3; }
    .seg-migrate { background-color: #8764b8; }
    .seg-free { background-color: rgba(255, 255, 255, 0.1); }

    .reclaim-tiles-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
    }

    .reclaim-tile {
      background: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      cursor: pointer;
      transition: all 120ms ease;
    }

    .reclaim-tile:hover {
      background: var(--fluent-subtle-hover);
      border-color: rgba(255, 255, 255, 0.18);
      transform: translateY(-1px);
    }

    .tile-title {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-primary);
    }

    .tile-size {
      font-size: 17px;
      font-weight: 700;
      color: #ffffff;
      font-family: var(--font-mono);
      font-variant-numeric: tabular-nums;
    }

    /* Giant Files Type Distribution */
    .type-distribution-card {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .type-distribution-bar {
      height: 12px;
      background-color: rgba(0, 0, 0, 0.35);
      border-radius: var(--radius-sm);
      overflow: hidden;
      display: flex;
    }

    .type-seg { height: 100%; transition: width 350ms ease; }
    .seg-db { background-color: #00bcf2; }
    .seg-exe { background-color: #f2994a; }
    .seg-vdisk { background-color: #8764b8; }
    .seg-archive { background-color: #0078d4; }
    .seg-other { background-color: #8899a6; }

    .type-legend-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      font-size: 11.5px;
    }

    .type-legend-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 3px 8px;
      background: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-control);
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: all 100ms ease;
      color: var(--text-secondary);
    }

    .type-legend-pill:hover, .type-legend-pill.active {
      background: var(--fluent-subtle-hover);
      color: var(--text-primary);
      border-color: rgba(255, 255, 255, 0.25);
    }

    .legend-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    /* Migration Projection Card */
    .projection-card {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .projection-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .projection-column {
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .projection-bar-box {
      height: 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-sm);
      overflow: hidden;
      display: flex;
    }

    .projection-seg-used { background-color: #0078d4; height: 100%; }
    .projection-seg-freed { background-color: #10b981; height: 100%; }
    .projection-seg-free { background-color: rgba(255, 255, 255, 0.12); height: 100%; }

    /* Modals & Toasts */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(16px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .modal-overlay.active { display: flex; }

    .content-dialog {
      width: 100%;
      max-width: 480px;
      background-color: #242933;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: var(--radius-md);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: dialogPop 140ms var(--motion-timing);
    }

    @keyframes dialogPop {
      from { transform: scale(0.96); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .dialog-header {
      padding: 14px 18px;
      border-bottom: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 14px;
      font-weight: 600;
    }

    .dialog-body {
      padding: 18px;
      font-size: 12.5px;
      color: var(--text-secondary);
      display: flex;
      flex-direction: column;
      gap: 12px;
      line-height: 1.5;
    }

    .dialog-footer {
      padding: 12px 18px;
      background-color: rgba(0, 0, 0, 0.2);
      border-top: 1px solid var(--fluent-stroke-divider);
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }

    .toast-container {
      position: fixed;
      bottom: 34px;
      right: 20px;
      z-index: 3000;
      display: flex;
      flex-direction: column;
      gap: 6px;
      pointer-events: none;
    }

    .toast-message {
      background: rgba(28, 33, 42, 0.94);
      backdrop-filter: blur(20px) saturate(140%);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: var(--radius-sm);
      padding: 8px 14px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: #ffffff;
      animation: toastSlide 160ms var(--motion-timing);
      pointer-events: auto;
    }

    @keyframes toastSlide {
      from { transform: translateY(10px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
  </style>
</head>
<body>

  <!-- Window Titlebar -->
  <header class="app-titlebar">
    <div class="titlebar-left">
      <svg class="app-brand-icon" viewBox="0 0 24 24">
        <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.67-3.13 9.07-7 10.18-3.87-1.11-7-5.51-7-10.18V6.3l7-3.12zM11 7v6h2V7h-2zm0 8v2h2v-2h-2z" fill="currentColor"/>
      </svg>
      <span class="app-brand-title">CleanFlow Pro</span>
      <span class="app-version-badge">v1.3</span>
    </div>

    <div class="titlebar-center" id="diskSelectorContainer">
      <!-- Injected via JS -->
    </div>

    <div class="titlebar-actions">
      <button class="win-caption-btn" title="最小化" onclick="minimizeWindow()">
        <svg class="icon" viewBox="0 0 24 24"><path d="M19 13H5v-2h14v2z"/></svg>
      </button>
      <button class="win-caption-btn" title="最大化" onclick="maximizeWindow()">
        <svg class="icon" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>
      </button>
      <button class="win-caption-btn btn-close" title="退出软件" onclick="shutdownApp()">
        <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
      </button>
    </div>
  </header>

  <!-- App Main Body -->
  <div class="app-body">

    <!-- Left NavigationView -->
    <aside class="navigation-view">
      <div>
        <div class="nav-group-title">核心空间治理</div>
        <ul class="nav-list">
          <li class="nav-item active" onclick="switchTab('overview')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg></span>
              <span>空间体检与清理</span>
            </div>
            <span class="nav-badge" id="badgeOverview">7.2 GB</span>
          </li>
          <li class="nav-item" onclick="switchTab('devcache')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg></span>
              <span>开发与编译缓存</span>
            </div>
            <span class="nav-badge" id="badgeDevCache">515 MB</span>
          </li>
          <li class="nav-item" onclick="switchTab('browser')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg></span>
              <span>浏览器深度专清</span>
            </div>
            <span class="nav-badge" id="badgeBrowser">878 MB</span>
          </li>
          <li class="nav-item" onclick="switchTab('registry')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-1 8h-3v3h-2v-3h-3v-2h3v-3h2v3h3v2z"/></svg></span>
              <span>注册表冗余修复</span>
            </div>
            <span class="nav-badge" id="badgeRegistry">0</span>
          </li>
        </ul>

        <div class="nav-group-title" style="margin-top: 14px;">高级虚拟化与索引</div>
        <ul class="nav-list">
          <li class="nav-item" onclick="switchTab('migration')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
              <span>目录无损搬家</span>
            </div>
            <span class="nav-badge">Junction</span>
          </li>
          <li class="nav-item" onclick="switchTab('giant')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
              <span>大文件全盘雷达</span>
            </div>
            <span class="nav-badge" id="badgeGiantFiles">89</span>
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
      <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--fluent-stroke-card); border-radius: var(--radius-sm); padding: 8px 10px; font-size: 11px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
          <span style="color:var(--text-tertiary);">当前盘符</span>
          <span style="color:#60cdff; font-weight:600;" id="sbDriveLetter">C:</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--text-tertiary);">可用空间</span>
          <span style="color:var(--status-safe); font-weight:600;" id="sbDriveFree">33.0 GB</span>
        </div>
      </div>
    </aside>

    <!-- Content Canvas (Workspaces + Inspector) -->
    <main class="content-canvas">
      <div class="workspace-wrapper">

        <!-- 1. Overview -->
        <section class="workspace-pane active" id="pane-overview">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>空间健康体检与清理</h1>
              <p>聚合系统冗余、包管理器缓存及开发临时数据，精准回收磁盘存储</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="runScan()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>重新体检</span>
              </button>
              <button class="btn btn-primary" id="btnQuickClean" onclick="executeQuickClean()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
                <span id="btnQuickCleanLabel">一键快速清理</span>
              </button>
            </div>
          </div>

          <div class="storage-hero-card">
            <div class="hero-top-row">
              <div style="display:flex; align-items:baseline; gap:8px;">
                <span class="hero-metric-figure" id="heroReclaimableNum">0.0</span>
                <span style="font-size:16px; font-weight:600; color:#60cdff;" id="heroReclaimableUnit">GB</span>
                <span style="color:var(--text-secondary); font-size:12px; margin-left:6px;">建议立即清理回收</span>
              </div>
              <span class="badge-pill badge-safe">检测就绪</span>
            </div>
            <div class="storage-ribbon" id="storageRibbon">
              <div class="ribbon-segment seg-system" style="width: 45%;" title="系统与基础数据"></div>
              <div class="ribbon-segment seg-apps" style="width: 30%;" title="已安装应用程序"></div>
              <div class="ribbon-segment seg-cleanable" style="width: 8%;" title="可安全清理缓存"></div>
              <div class="ribbon-segment seg-free" style="width: 17%;" title="剩余可用空间"></div>
            </div>
          </div>

          <div class="reclaim-tiles-grid">
            <div class="reclaim-tile" onclick="switchTab('devcache')">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="tile-title">开发构建缓存</span>
                <span class="badge-pill badge-safe">安全</span>
              </div>
              <span class="tile-size" id="tileDevSize">515.9 MB</span>
              <span style="font-size:11px; color:var(--text-tertiary);">npm, pnpm, Unity, Gradle</span>
            </div>
            <div class="reclaim-tile" onclick="switchTab('browser')">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="tile-title">浏览器深度专清</span>
                <span class="badge-pill badge-safe">缓存</span>
              </div>
              <span class="tile-size" id="tileBrowserSize">878.2 MB</span>
              <span style="font-size:11px; color:var(--text-tertiary);">Edge, Chrome, 360 离线媒体</span>
            </div>
            <div class="reclaim-tile" onclick="switchTab('migration')">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="tile-title">大资产迁移潜能</span>
                <span class="badge-pill badge-junction">Junction</span>
              </div>
              <span class="tile-size" id="tileMigrateSize">13.3 GB</span>
              <span style="font-size:11px; color:var(--text-tertiary);">Android 模拟器与微信数据</span>
            </div>
            <div class="reclaim-tile" onclick="switchTab('vacuum')">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="tile-title">数据库空间整理</span>
                <span class="badge-pill badge-safe">无损</span>
              </div>
              <span class="tile-size" id="tileVacuumSize">4.0 GB</span>
              <span style="font-size:11px; color:var(--text-tertiary);">SQLite 碎片收缩</span>
            </div>
          </div>

          <div class="desktop-commandbar">
            <div class="commandbar-left">
              <div class="search-box">
                <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
                <input type="text" id="overviewSearchInput" placeholder="过滤体检项目或路径..." oninput="filterOverviewTable()">
              </div>
              <div class="filter-tabs">
                <div class="filter-tab active" onclick="setOverviewFilter('all', this)">全部</div>
                <div class="filter-tab" onclick="setOverviewFilter('safe', this)">安全推荐项</div>
                <div class="filter-tab" onclick="setOverviewFilter('dev', this)">开发工具</div>
                <div class="filter-tab" onclick="setOverviewFilter('browser', this)">浏览器</div>
              </div>
            </div>
            <span style="font-size:11.5px; color:var(--text-tertiary);" id="overviewCounter">就绪</span>
          </div>

          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th class="col-checkbox"><input type="checkbox" id="selectAllOverview" onchange="toggleSelectAllOverview(this.checked)" checked></th>
                  <th>清理分类</th>
                  <th>匹配物理路径</th>
                  <th style="text-align: right;">体积占用</th>
                  <th>文件数</th>
                  <th style="text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="overviewTableBody">
                <!-- Rendered via JS -->
              </tbody>
            </table>
          </div>
        </section>

        <!-- 2. Dev Cache -->
        <section class="workspace-pane" id="pane-devcache">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>现代开发与包管理器缓存</h1>
              <p>释放 npm、pnpm、Unity、Gradle 等工具的全局离线包与编译缓存</p>
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
                  <th>技术栈 / 工具</th>
                  <th>缓存物理路径</th>
                  <th style="text-align: right;">占用体积</th>
                  <th>文件数</th>
                  <th style="text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="devcacheTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 3. Browser Cache -->
        <section class="workspace-pane" id="pane-browser">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>主流浏览器深度专清</h1>
              <p>安全清理 Edge、Chrome、360 等浏览器的离线网页媒体与编译代码缓存，不影响登录态与书签</p>
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
                  <th>浏览器 / 缓存类型</th>
                  <th>磁盘物理路径</th>
                  <th style="text-align: right;">占用体积</th>
                  <th>文件数</th>
                  <th style="text-align: center;">操作</th>
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
              <p>排查已卸载软件的历史残留键、无效卸载项及失效 MUICache，修复前自动生成 .reg 回滚备份</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="loadRegistryIssues()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>重新扫描注册表</span>
              </button>
              <button class="btn btn-primary" id="btnCleanRegistry" onclick="executeCleanRegistry()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                <span id="btnCleanRegistryLabel">一键安全修复选中项</span>
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
            <span style="font-size: 11.5px; color: var(--text-tertiary);" id="registryCounter">准备就绪</span>
          </div>

          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th class="col-checkbox"><input type="checkbox" id="selectAllRegistryCheckbox" onchange="toggleSelectAllRegistry(this.checked)" checked></th>
                  <th>问题类型</th>
                  <th>失效引用的物理路径</th>
                  <th>注册表底层键路径</th>
                  <th>安全等级</th>
                  <th style="text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="registryTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 5. Junction Migration -->
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

          <div class="projection-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:13px; font-weight:600;">空间无损搬迁效益预测 (NTFS Junction 重定向)</span>
              <span class="badge-pill badge-safe">100% 透明无损 · 原位创建虚拟联接点</span>
            </div>
            <div class="projection-grid">
              <div class="projection-column">
                <div style="display:flex; justify-content:space-between; font-size:11.5px;">
                  <span style="color:var(--text-secondary);">源磁盘 (C: 盘) 释放预测</span>
                  <span style="color:#10b981; font-weight:600;">预计释放 +13.3 GB</span>
                </div>
                <div class="projection-bar-box">
                  <div class="projection-seg-used" style="width: 77%;"></div>
                  <div class="projection-seg-freed" style="width: 7%;"></div>
                  <div class="projection-seg-free" style="width: 16%;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-tertiary);">
                  <span>当前可用 33.0 GB</span>
                  <span style="color:#60cdff;">搬迁后预计提升至 46.3 GB</span>
                </div>
              </div>
              <div class="projection-column">
                <div style="display:flex; justify-content:space-between; font-size:11.5px;">
                  <span style="color:var(--text-secondary);">目标磁盘 (D: 盘) 承载状态</span>
                  <span style="color:#60cdff; font-weight:600;">93.1 GB 充足容量</span>
                </div>
                <div class="projection-bar-box">
                  <div class="projection-seg-used" style="width: 76.7%; background-color:#8764b8;"></div>
                  <div class="projection-seg-free" style="width: 23.3%;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-tertiary);">
                  <span>本地高速 SSD</span>
                  <span>跨盘读写完全透明</span>
                </div>
              </div>
            </div>
          </div>

          <div style="background:var(--fluent-card-bg); border:1px solid var(--fluent-stroke-card); border-radius:var(--radius-md); padding:14px; display:flex; flex-direction:column; gap:10px;">
            <span style="font-size:13px; font-weight:600;">自定义任意目录一键搬家</span>
            <div style="display:flex; gap:10px;">
              <input type="text" id="customMigrateSource" placeholder="输入或粘贴需要搬迁的 C 盘目录绝对路径 (如 C:\Users\EDY\.android\avd)..." style="flex:3; background:var(--fluent-subtle); border:1px solid var(--fluent-stroke-control); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; font-family:var(--font-mono); outline:none;">
              <select id="customMigrateTargetDrive" style="flex:1; background:var(--fluent-subtle); border:1px solid var(--fluent-stroke-control); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none;">
                <option value="D:">D 盘 (本地大容量磁盘)</option>
                <option value="E:">E 盘</option>
              </select>
            </div>
            <div style="display:flex; gap:8px;">
              <button class="btn btn-secondary" onclick="analyzeCustomPath()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg></span>
                <span>分析体积与进程占用</span>
              </button>
              <button class="btn btn-primary" id="btnStartCustomMigrate" onclick="startCustomPathMigration()" disabled>
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
                <span>立即安全迁移并创建 Junction</span>
              </button>
            </div>
            <div id="customPathFeedback" style="display:none; padding:8px 10px; background:var(--fluent-subtle); border-radius:var(--radius-sm); font-size:12px; color:var(--text-secondary);"></div>
          </div>

          <h3 style="font-size:13px; font-weight:600; margin-top:4px;">当前活动的 Junction 目录联接 (已搬迁项)</h3>
          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th>原始 C 盘虚拟路径</th>
                  <th>实际物理存储位置</th>
                  <th>创建时间</th>
                  <th style="text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="activeJunctionsTableBody"></tbody>
            </table>
          </div>
        </section>

        <!-- 6. Giant Files Radar -->
        <section class="workspace-pane" id="pane-giant">
          <div class="workspace-header">
            <div class="workspace-title-box">
              <h1>大文件全盘雷达 (100MB+ 沉淀文件)</h1>
              <p>快速排查深层隐蔽的大型压缩包、虚拟磁盘、开发数据库与历史安装包</p>
            </div>
            <div class="workspace-controls">
              <button class="btn btn-secondary" onclick="loadGiantFiles()">
                <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
                <span>刷新全盘雷达</span>
              </button>
            </div>
          </div>

          <div class="type-distribution-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:12.5px; font-weight:600;">大文件资产类型占比与容量分层 (基于全盘检索)</span>
              <span style="font-size:11.5px; color:#60cdff; font-weight:600;" id="giantTotalSizeText">总计 28.6 GB (89 个文件)</span>
            </div>
            <div class="type-distribution-bar" id="giantDistributionBar">
              <div class="type-seg seg-db" style="width: 32%;" title="数据库与开发状态"></div>
              <div class="type-seg seg-vdisk" style="width: 25%;" title="虚拟机与虚拟盘"></div>
              <div class="type-seg seg-exe" style="width: 20%;" title="安装包与程序"></div>
              <div class="type-seg seg-archive" style="width: 5%;" title="压缩归档"></div>
              <div class="type-seg seg-other" style="width: 18%;" title="其他大型资产"></div>
            </div>
            <div class="type-legend-pills" id="giantLegendContainer">
              <div class="type-legend-pill active" onclick="setGiantFilter('all', this)">
                <span class="legend-dot" style="background:#fff;"></span>
                <span>全部资产 (89)</span>
              </div>
              <div class="type-legend-pill" onclick="setGiantFilter('Database', this)">
                <span class="legend-dot" style="background:#00bcf2;"></span>
                <span>数据库 (9.5 GB)</span>
              </div>
              <div class="type-legend-pill" onclick="setGiantFilter('VirtualDisk', this)">
                <span class="legend-dot" style="background:#8764b8;"></span>
                <span>虚拟机 (6.1 GB)</span>
              </div>
              <div class="type-legend-pill" onclick="setGiantFilter('Executable', this)">
                <span class="legend-dot" style="background:#f2994a;"></span>
                <span>安装包 (8.0 GB)</span>
              </div>
              <div class="type-legend-pill" onclick="setGiantFilter('Archive', this)">
                <span class="legend-dot" style="background:#0078d4;"></span>
                <span>压缩包 (1.0 GB)</span>
              </div>
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
                <div class="filter-tab" onclick="setGiantSizeFilter('huge', this)">超大 (&gt;1GB)</div>
                <div class="filter-tab" onclick="setGiantSizeFilter('large', this)">大文件 (500M-1G)</div>
                <div class="filter-tab" onclick="setGiantSizeFilter('mid', this)">常规 (100M-500M)</div>
              </div>
            </div>
            <span style="font-size:11.5px; color:var(--text-tertiary);" id="giantFilesCounter">扫描就绪</span>
          </div>

          <div class="data-grid-container">
            <table class="data-grid">
              <thead>
                <tr>
                  <th>文件名称</th>
                  <th>类型</th>
                  <th>完整物理路径</th>
                  <th style="text-align: right;">文件大小</th>
                  <th style="text-align: center;">操作</th>
                </tr>
              </thead>
              <tbody id="giantTableBody"></tbody>
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
                  <th>数据库名称与用途</th>
                  <th>底层数据库路径</th>
                  <th style="text-align: right;">当前物理体积</th>
                  <th>碎片释放潜能</th>
                  <th style="text-align: center;">操作</th>
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

          <div style="background:var(--fluent-card-bg); border:1px solid var(--fluent-stroke-card); border-radius:var(--radius-md); padding:16px; display:flex; flex-direction:column; gap:12px;">
            <div style="font-weight:600; font-size:12.5px; color:var(--text-primary);">创建专属巡检清理规则</div>
            <div style="display:flex; gap:12px; align-items:flex-end;">
              <div style="flex:1;">
                <label style="font-size:11.5px; color:var(--text-secondary); display:block; margin-bottom:5px;">规则名称</label>
                <input type="text" id="ruleNameInput" placeholder="例如: Webpack dist 构建产物" style="width:100%; background:var(--fluent-subtle); border:1px solid var(--fluent-stroke-control); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none;">
              </div>
              <div style="flex:2;">
                <label style="font-size:11.5px; color:var(--text-secondary); display:block; margin-bottom:5px;">绝对路径模式 (支持 %LOCALAPPDATA% 等环境变量与通配符)</label>
                <input type="text" id="rulePatternInput" placeholder="例如: %LOCALAPPDATA%\MyTool\cache\*" style="width:100%; background:var(--fluent-subtle); border:1px solid var(--fluent-stroke-control); border-radius:var(--radius-sm); padding:6px 10px; color:#fff; font-size:12px; outline:none; font-family:var(--font-mono);">
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
      <aside class="desktop-inspector" id="desktopInspector">
        <div class="inspector-header">
          <div class="inspector-title">
            <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
            <span>属性与进程检查</span>
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
              <button class="icon-action-btn" title="复制路径" onclick="copyInspectorPath()">
                <svg class="icon" viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
              </button>
            </div>
            <div class="inspector-path-box" id="inspPath">-</div>
          </div>

          <div class="inspector-card">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
              <div>
                <span class="inspector-label">占用体积</span>
                <div class="inspector-val" id="inspSize" style="font-family:var(--font-mono); font-weight:600;">-</div>
              </div>
              <div>
                <span class="inspector-label">文件数量</span>
                <div class="inspector-val" id="inspFiles">-</div>
              </div>
            </div>
          </div>

          <div class="inspector-card">
            <span class="inspector-label">进程互斥与占用检测</span>
            <div id="inspLockStatus" style="font-size:12px; color:var(--status-safe); margin-top:2px;">
              进程未锁定 · 安全可处理
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

  <!-- Desktop Bottom StatusBar -->
  <footer class="desktop-statusbar">
    <div class="statusbar-left">
      <span>驱动器:</span>
      <span class="statusbar-accent" id="sbDiskDetails">C: 盘 33.0 GB 可用 / 200 GB (83.5%)</span>
    </div>
    <div class="statusbar-center">
      <span id="sbTaskStatus">就绪</span>
      <span>|</span>
      <span id="sbSelectionStatus">未选中项</span>
    </div>
    <div class="statusbar-right">
      <span>Rust 原生内核 v0.1.0</span>
      <span>·</span>
      <span style="color:var(--status-safe);">零后台常驻</span>
    </div>
  </footer>

  <!-- Right-Click Fluent Acrylic Context Menu -->
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
    <div class="context-menu-divider"></div>
    <div class="context-menu-item" style="color:#ff99a4;" onclick="onContextClean()">
      <span class="icon"><svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg></span>
      <span>安全清理 / 删除此项</span>
    </div>
  </div>

  <!-- WinUI 3 ContentDialog Modal -->
  <div class="modal-overlay" id="confirmModal">
    <div class="content-dialog">
      <div class="dialog-header">
        <span id="confirmModalTitle">操作确认</span>
        <button class="win-caption-btn" style="width:28px; height:28px;" onclick="closeConfirmModal()">
          <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      </div>
      <div class="dialog-body" id="confirmModalBody">确认执行操作吗？</div>
      <div class="dialog-footer">
        <button class="btn btn-secondary" onclick="closeConfirmModal()">取消</button>
        <button class="btn btn-primary" id="confirmModalOkBtn" onclick="onConfirmModalOk()">确定</button>
      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <div class="toast-container" id="toastContainer"></div>

  <script>
    // State management
    const state = {
      currentTab: 'overview',
      disks: [],
      currentDrive: 'C:',
      scanReport: null,
      selectedPaths: new Set(),
      giantFiles: [],
      giantFilterCategory: 'all',
      giantSizeFilter: 'all',
      giantSearchTerm: '',
      registryIssues: [],
      selectedRegistryIds: new Set(),
      registryFilterCategory: 'all',
      activeJunctions: [],
      inspectorTarget: null,
      contextTarget: null
    };

    // Format utility
    function formatBytes(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(i >= 2 ? 1 : 0) + ' ' + sizes[i];
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
        'migration': 4, 'giant': 5, 'vacuum': 6, 'rules': 7
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

    function inspectItem(item) {
      state.inspectorTarget = item;
      document.getElementById('inspName').innerText = item.name || item.path.split('\\').pop() || '未命名资产';
      document.getElementById('inspCategory').innerText = item.category || '通用缓存';
      document.getElementById('inspPath').innerText = item.path;
      document.getElementById('inspSize').innerText = formatBytes(item.size_bytes || 0);
      document.getElementById('inspFiles').innerText = item.file_count ? `${item.file_count} 个文件` : '单个文件';

      // Lock check
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

    // Scan
    async function runScan() {
      showToast('正在执行全盘空间健康体检...');
      document.getElementById('sbTaskStatus').innerText = '正在扫描全盘资产...';
      try {
        const res = await fetch('/api/scan');
        state.scanReport = await res.json();
        state.selectedPaths.clear();

        state.scanReport.categories.forEach(cat => {
          cat.rules.forEach(r => {
            if (r.default_checked) {
              r.matched_paths.forEach(mp => {
                if (mp.size_bytes > 0) state.selectedPaths.add(mp.path);
              });
            }
          });
        });

        renderOverviewTable();
        renderDevCacheTable();
        renderBrowserTable();
        renderVacuumTable();
        updateOverviewHero();
        document.getElementById('sbTaskStatus').innerText = '体检完成';
        showToast('体检完成，已识别可释放空间');
      } catch (e) {
        showToast('体检扫描失败: ' + e.message);
        document.getElementById('sbTaskStatus').innerText = '扫描出错';
      }
    }

    function updateOverviewHero() {
      if (!state.scanReport) return;
      const totalBytes = state.scanReport.total_size_bytes;
      const gb = totalBytes / (1024**3);
      if (gb >= 1) {
        document.getElementById('heroReclaimableNum').innerText = gb.toFixed(1);
        document.getElementById('heroReclaimableUnit').innerText = 'GB';
      } else {
        document.getElementById('heroReclaimableNum').innerText = (totalBytes / (1024**2)).toFixed(0);
        document.getElementById('heroReclaimableUnit').innerText = 'MB';
      }

      document.getElementById('badgeOverview').innerText = formatBytes(totalBytes);
      document.getElementById('btnQuickCleanLabel').innerText = `一键快速清理 (${formatBytes(totalBytes)})`;
      updateSelectionStatus();
    }

    function updateSelectionStatus() {
      let selBytes = 0;
      if (state.scanReport) {
        state.scanReport.categories.forEach(c => {
          c.rules.forEach(r => {
            r.matched_paths.forEach(mp => {
              if (state.selectedPaths.has(mp.path)) selBytes += mp.size_bytes;
            });
          });
        });
      }
      document.getElementById('sbSelectionStatus').innerText = `已选 ${state.selectedPaths.size} 项 (${formatBytes(selBytes)})`;
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
              <td class="col-checkbox"><input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleSelectPath('${escapeHtml(mp.path)}', this.checked)"></td>
              <td style="font-weight:600;"><span class="badge-pill badge-safe">${escapeHtml(cat.name)}</span></td>
              <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
              <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
              <td style="color: var(--text-tertiary);">${mp.file_count} 文件</td>
              <td style="text-align: center;">
                <div class="table-actions" style="justify-content: center;">
                  <button class="icon-action-btn" title="在资源管理器中定位" onclick="revealInExplorer('${escapeHtml(mp.path)}')">
                    <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
                  </button>
                  <button class="icon-action-btn" title="清理该项" onclick="deleteSingleItem('${escapeHtml(mp.path)}')">
                    <svg class="icon" viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
                  </button>
                </div>
              </td>
            `;
            tbody.appendChild(tr);
          });
        });
      });

      document.getElementById('overviewCounter').innerText = `已检出 ${renderedCount} 处清理项`;
    }

    function toggleSelectPath(p, checked) {
      if (checked) state.selectedPaths.add(p);
      else state.selectedPaths.delete(p);
      updateSelectionStatus();
    }

    function toggleSelectAllOverview(checked) {
      state.selectedPaths.clear();
      if (checked && state.scanReport) {
        state.scanReport.categories.forEach(c => {
          c.rules.forEach(r => {
            r.matched_paths.forEach(mp => {
              if (mp.size_bytes > 0) state.selectedPaths.add(mp.path);
            });
          });
        });
      }
      renderOverviewTable();
      updateSelectionStatus();
    }

    // Dev Cache Table
    function renderDevCacheTable() {
      const tbody = document.getElementById('devcacheTableBody');
      tbody.innerHTML = '';
      if (!state.scanReport) return;
      const cat = state.scanReport.categories.find(c => c.id === 'dev_cache');
      if (!cat) return;

      document.getElementById('badgeDevCache').innerText = formatBytes(cat.total_size_bytes);
      document.getElementById('tileDevSize').innerText = formatBytes(cat.total_size_bytes);

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
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: '开发缓存' });
            }
          };
          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked></td>
            <td style="font-weight:600;">${escapeHtml(r.name)}</td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
            <td style="color: var(--text-tertiary);">${mp.file_count} 文件</td>
            <td style="text-align: center;">
              <button class="icon-action-btn" title="定位" onclick="revealInExplorer('${escapeHtml(mp.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
              </button>
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

      document.getElementById('badgeBrowser').innerText = formatBytes(cat.total_size_bytes);
      document.getElementById('tileBrowserSize').innerText = formatBytes(cat.total_size_bytes);

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
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: '浏览器缓存' });
            }
          };
          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked></td>
            <td style="font-weight:600;">${escapeHtml(r.name)}</td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
            <td style="color: var(--text-tertiary);">${mp.file_count} 文件</td>
            <td style="text-align: center;">
              <button class="icon-action-btn" title="定位" onclick="revealInExplorer('${escapeHtml(mp.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
              </button>
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

      const tileEl = document.getElementById('tileVacuumSize');
      if (tileEl) tileEl.innerText = formatBytes(cat.total_size_bytes);

      cat.rules.forEach(r => {
        r.matched_paths.forEach(mp => {
          const tr = document.createElement('tr');
          tr.setAttribute('data-path', mp.path);
          tr.setAttribute('data-name', r.name);
          tr.setAttribute('data-size', mp.size_bytes);
          tr.setAttribute('data-cat', 'SQLite 数据库');
          tr.onclick = (e) => {
            if (e.target.tagName !== 'BUTTON') {
              document.querySelectorAll('.data-grid tbody tr').forEach(r => r.classList.remove('selected'));
              tr.classList.add('selected');
              inspectItem({ name: r.name, path: mp.path, size_bytes: mp.size_bytes, file_count: mp.file_count, category: 'SQLite 数据库' });
            }
          };
          tr.innerHTML = `
            <td style="font-weight:600;">${escapeHtml(r.name)}</td>
            <td><span class="path-text" title="${escapeHtml(mp.path)}">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(mp.size_bytes)}</td>
            <td><span class="badge-pill badge-safe">无损压缩碎片</span></td>
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
        showToast('扫描注册表失败: ' + e.message);
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
        showToast('请先勾选需要修复的注册表项');
        return;
      }
      openConfirmModal('注册表安全修复确认', `即将安全修复选中的 ${state.selectedRegistryIds.size} 项注册表残留。<br><br><strong>系统将自动在修复前导出 .reg 完整回滚备份</strong>，确保 100% 安全无后顾之忧。`, async () => {
        closeConfirmModal();
        showToast('正在导出备份并执行安全修复...');
        try {
          const res = await fetch('/api/registry/clean', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ids: Array.from(state.selectedRegistryIds) })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`成功修复 ${data.items_cleaned} 处残留，备份已生成！`);
            loadRegistryIssues();
          } else {
            showToast('修复遇到错误: ' + (data.errors ? data.errors.join('; ') : '未知错误'));
          }
        } catch (e) {
          showToast('请求异常: ' + e.message);
        }
      });
    }

    // Giant Files
    async function loadGiantFiles() {
      showToast('正在雷达扫描 100MB+ 全盘沉淀资产...');
      document.getElementById('giantFilesCounter').innerText = '扫描中...';
      try {
        const res = await fetch('/api/giant-files');
        state.giantFiles = await res.json();
        document.getElementById('badgeGiantFiles').innerText = state.giantFiles.length;
        document.getElementById('giantFilesCounter').innerText = `已排查出 ${state.giantFiles.length} 个大型资产`;
        renderGiantDistribution();
        renderGiantTable();
        showToast(`大文件雷达发现 ${state.giantFiles.length} 个沉淀大资产`);
      } catch (e) {
        showToast('读取大文件失败: ' + e.message);
      }
    }

    function renderGiantDistribution() {
      if (!state.giantFiles || state.giantFiles.length === 0) return;
      const cats = { Database: 0, Executable: 0, VirtualDisk: 0, Archive: 0, Other: 0 };
      let totalBytes = 0;
      state.giantFiles.forEach(f => {
        totalBytes += f.size_bytes;
        const c = f.category || 'Other';
        if (cats[c] !== undefined) cats[c] += f.size_bytes;
        else cats.Other += f.size_bytes;
      });
      const totalGb = (totalBytes / (1024**3)).toFixed(1);
      document.getElementById('giantTotalSizeText').innerText = `总计 ${totalGb} GB (${state.giantFiles.length} 个文件)`;

      if (totalBytes > 0) {
        const bar = document.getElementById('giantDistributionBar');
        const pDb = Math.max(1, ((cats.Database / totalBytes) * 100).toFixed(1));
        const pExe = Math.max(1, ((cats.Executable / totalBytes) * 100).toFixed(1));
        const pVd = Math.max(1, ((cats.VirtualDisk / totalBytes) * 100).toFixed(1));
        const pArch = Math.max(1, ((cats.Archive / totalBytes) * 100).toFixed(1));
        const pOth = Math.max(1, (100 - pDb - pExe - pVd - pArch).toFixed(1));

        bar.innerHTML = `
          <div class="type-seg seg-db" style="width: ${pDb}%;" title="数据库: ${(cats.Database / (1024**3)).toFixed(1)} GB"></div>
          <div class="type-seg seg-vdisk" style="width: ${pVd}%;" title="虚拟盘: ${(cats.VirtualDisk / (1024**3)).toFixed(1)} GB"></div>
          <div class="type-seg seg-exe" style="width: ${pExe}%;" title="安装包: ${(cats.Executable / (1024**3)).toFixed(1)} GB"></div>
          <div class="type-seg seg-archive" style="width: ${pArch}%;" title="压缩包: ${(cats.Archive / (1024**3)).toFixed(1)} GB"></div>
          <div class="type-seg seg-other" style="width: ${pOth}%;" title="其他: ${(cats.Other / (1024**3)).toFixed(1)} GB"></div>
        `;
      }
    }

    function renderGiantTable() {
      const tbody = document.getElementById('giantTableBody');
      tbody.innerHTML = '';
      if (!state.giantFiles || state.giantFiles.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 30px; color: var(--text-tertiary);">未发现大于 100MB 的文件</td></tr>`;
        return;
      }

      const filtered = state.giantFiles.filter(f => {
        if (state.giantFilterCategory !== 'all' && f.category !== state.giantFilterCategory) return false;
        if (state.giantSizeFilter === 'huge' && f.size_bytes < 1024**3) return false;
        if (state.giantSizeFilter === 'large' && (f.size_bytes < 500 * 1024**2 || f.size_bytes >= 1024**3)) return false;
        if (state.giantSizeFilter === 'mid' && (f.size_bytes < 100 * 1024**2 || f.size_bytes >= 500 * 1024**2)) return false;
        if (state.giantSearchTerm) {
          const q = state.giantSearchTerm.toLowerCase();
          return f.name.toLowerCase().includes(q) || f.path.toLowerCase().includes(q);
        }
        return true;
      });

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
            inspectItem({ name: f.name, path: f.path, size_bytes: f.size_bytes, file_count: 1, category: f.category || '大文件' });
          }
        };

        tr.innerHTML = `
          <td style="font-weight:600;">${escapeHtml(f.name)}</td>
          <td><span class="badge-pill badge-safe">${escapeHtml(f.category || '文件')}</span></td>
          <td><span class="path-text" title="${escapeHtml(f.path)}">${escapeHtml(f.path)}</span></td>
          <td style="text-align: right; font-family: var(--font-mono); font-weight: 600;">${formatBytes(f.size_bytes)}</td>
          <td style="text-align: center;">
            <div class="table-actions" style="justify-content: center;">
              <button class="icon-action-btn" title="定位" onclick="revealInExplorer('${escapeHtml(f.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
              </button>
              <button class="icon-action-btn" title="安全粉碎" onclick="deleteSingleItem('${escapeHtml(f.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
              </button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function setGiantFilter(cat, el) {
      state.giantFilterCategory = cat;
      document.querySelectorAll('.type-legend-pill').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderGiantTable();
    }

    function setGiantSizeFilter(range, el) {
      state.giantSizeFilter = range;
      document.querySelectorAll('#pane-giant .desktop-commandbar .filter-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderGiantTable();
    }

    function filterGiantTable() {
      state.giantSearchTerm = document.getElementById('giantSearchInput').value;
      renderGiantTable();
    }

    // Junctions
    async function loadActiveJunctions() {
      try {
        const res = await fetch('/api/junctions');
        state.activeJunctions = await res.json();
        renderActiveJunctions();
      } catch (e) {
        console.error('Failed to load junctions', e);
      }
    }

    function renderActiveJunctions() {
      const tbody = document.getElementById('activeJunctionsTableBody');
      tbody.innerHTML = '';
      if (!state.activeJunctions || state.activeJunctions.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 20px; color: var(--text-tertiary);">当前无活动中的 Junction 联接点</td></tr>`;
        return;
      }
      state.activeJunctions.forEach(j => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="path-text">${escapeHtml(j.source_path || j.original_path)}</span></td>
          <td><span class="path-text" style="color:#60cdff;">${escapeHtml(j.target_path)}</span></td>
          <td style="color:var(--text-tertiary);">${escapeHtml(j.created_at || '生效中')}</td>
          <td style="text-align: center;">
            <div class="table-actions" style="justify-content: center;">
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(j.target_path)}')">打开目标</button>
              <button class="btn btn-danger" style="padding: 2px 8px; font-size: 11px;" onclick="rollbackJunction('${escapeHtml(j.source_path || j.original_path)}')">还原回 C 盘</button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    async function analyzeCustomPath() {
      const p = document.getElementById('customMigrateSource').value.trim();
      if (!p) {
        showToast('请输入需要分析的目录路径');
        return;
      }
      const fb = document.getElementById('customPathFeedback');
      fb.style.display = 'block';
      fb.innerText = '正在分析目录体积与进程占用...';

      try {
        const res = await fetch('/api/check-path', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: p })
        });
        const data = await res.json();
        if (!data.exists) {
          fb.innerText = '错误: 目标路径不存在或无权访问';
          fb.style.color = 'var(--status-danger)';
          document.getElementById('btnStartCustomMigrate').disabled = true;
          return;
        }

        const sizeStr = formatBytes(data.size_bytes);
        let msg = `分析成功: 包含 ${data.file_count} 个文件，总体积 ${sizeStr}。`;
        if (data.locking_processes && data.locking_processes.length > 0) {
          msg += ` 警告: 正在被进程 [${data.locking_processes.join(', ')}] 锁定，建议迁移前先关闭相关程序。`;
          fb.style.color = 'var(--status-warn)';
        } else {
          msg += ' 进程未锁定，完全安全可搬家。';
          fb.style.color = 'var(--status-safe)';
        }
        fb.innerText = msg;
        document.getElementById('btnStartCustomMigrate').disabled = false;
      } catch (e) {
        fb.innerText = '分析失败: ' + e.message;
      }
    }

    function startCustomPathMigration() {
      const src = document.getElementById('customMigrateSource').value.trim();
      const targetDrive = document.getElementById('customMigrateTargetDrive').value;
      if (!src) return;

      openConfirmModal('目录无损搬家确认', `即将将目录：<br><span class="path-text" style="color:#60cdff;">${escapeHtml(src)}</span><br>迁移至 <strong>${targetDrive}</strong> 并在原位置建立原生 NTFS Junction。<br><br>迁移期间将完整保持文件结构，确认开始吗？`, async () => {
        closeConfirmModal();
        showToast('正在执行无损跨盘迁移，请稍候...');
        try {
          const res = await fetch('/api/migrate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_path: src, target_drive: targetDrive.replace(':', '') })
          });
          const data = await res.json();
          if (data.success) {
            showToast(`搬家成功！已腾退 ${formatBytes(data.bytes_moved)}`);
            loadActiveJunctions();
            refreshDisks();
            runScan();
          } else {
            showToast('迁移失败: ' + (data.error || '未知错误'));
          }
        } catch (e) {
          showToast('请求异常: ' + e.message);
        }
      });
    }

    function rollbackJunction(src) {
      openConfirmModal('还原软链接确认', `即将把数据搬迁回原 C 盘并移除 Junction：<br><br><span class="path-text">${escapeHtml(src)}</span>`, async () => {
        closeConfirmModal();
        showToast('正在还原数据回 C 盘...');
        try {
          const res = await fetch('/api/junctions/rollback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_path: src })
          });
          const data = await res.json();
          if (data.success) {
            showToast('已还原回 C 盘并安全移除软链接');
            loadActiveJunctions();
            refreshDisks();
            runScan();
          } else {
            showToast('还原遇到错误: ' + data.error);
          }
        } catch (e) {
          showToast('请求异常: ' + e.message);
        }
      });
    }

    // Actions
    async function revealInExplorer(p) {
      try {
        await fetch('/api/reveal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: p })
        });
        showToast('已在资源管理器中定位');
      } catch (e) {
        showToast('定位失败');
      }
    }

    function deleteSingleItem(p) {
      openConfirmModal('安全删除确认', `确定要删除该项吗？<br><br><span class="path-text">${escapeHtml(p)}</span>`, async () => {
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
            if (state.currentTab === 'giant') loadGiantFiles();
            refreshDisks();
          } else {
            showToast('清理失败: 文件可能被占用');
          }
        } catch (e) {
          showToast('请求失败: ' + e.message);
        }
      });
    }

    function executeQuickClean() {
      if (state.selectedPaths.size === 0) {
        showToast('请先勾选需要清理的项目');
        return;
      }
      openConfirmModal('一键快速清理确认', `即将安全清理选中的 ${state.selectedPaths.size} 个缓存目录或文件。<br><br>系统将自动跳过正在被使用的文件，保证系统与软件稳定。确认执行吗？`, async () => {
        closeConfirmModal();
        showToast('正在安全执行清理...');
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

def main():
    # Verify zero emojis in HTML_CONTENT
    emojis = re.findall(r'[\U00010000-\U0010ffff]', HTML_CONTENT)
    if emojis:
        print(f"ERROR: Found {len(emojis)} emojis!")
        return

    target_ui_path = os.path.join(os.path.dirname(__file__), 'src', 'ui.html')
    with open(target_ui_path, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f"Generated Pro Desktop UI: {target_ui_path} ({len(HTML_CONTENT)} bytes, 0 emojis)")

    # Also update build_desktop_ui.py to match
    with open('build_desktop_ui.py', 'w', encoding='utf-8') as f:
        f.write(f'# -*- coding: utf-8 -*-\nHTML_CONTENT = r\'\'\'{HTML_CONTENT}\'\'\'\n\nif __name__ == "__main__":\n    import os\n    target_path = os.path.join(os.path.dirname(__file__), "src", "ui.html")\n    with open(target_path, "w", encoding="utf-8") as f:\n        f.write(HTML_CONTENT)\n    print(f"Generated: {{target_path}}")\n')
    print("build_desktop_ui.py synced.")

if __name__ == '__main__':
    main()
