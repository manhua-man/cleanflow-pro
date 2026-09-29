# -*- coding: utf-8 -*-
"""
CleanFlow Pro - Windows 11 Fluent 2 Consumer Desktop Interface Generator
Built according to local APP_Studio & frontend-design & winui specifications.
Strict Rules:
- NO EMOJI IN CODE OR UI.
- Genuine Windows 11 Fluent 2 Desktop Software Vernacular:
  * Titlebar with drag region, disk switcher, window controls
  * NavigationView sidebar with active indicator pills and badge counts
  * Storage Ribbon & Health Hero (boldness in one place)
  * Dedicated workspaces:
    1. 空间体检与清理 (Overview & Clean)
    2. 开发与编译缓存 (Dev Stacks)
    3. 浏览器深度专清 (Browser Hygiene)
    4. 注册表冗余修复 (Registry Cleaner & Backup)
    5. 目录无损搬家 (NTFS Junction Migration)
    6. 大文件雷达 (Giant Files Analyzer >100MB)
    7. 数据库碎片收缩 (SQLite Vacuum)
    8. 自定义规则引擎 (Rule Studio)
  * Native WinUI ContentDialog modals, InfoBar banners, and Toast notifications
- Zero runtime dependencies, completely self-contained offline HTML.
"""

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CleanFlow Pro - Windows 智能空间管家</title>
  <style>
    /* ==========================================================================
       Windows 11 Fluent 2 Design System (APP_Studio Grounded)
       Tokens derived from winui.csv & styles.csv
       ========================================================================== */
    :root {
      /* Surface & Mica Backdrops */
      --fluent-mica-base: #1c1c1c;
      --fluent-mica-alt: #202020;
      --fluent-layer-base: #242424;
      --fluent-card-bg: #2b2b2b;
      --fluent-card-hover: #323232;
      --fluent-card-active: #272727;
      --fluent-subtle: rgba(255, 255, 255, 0.05);
      --fluent-subtle-hover: rgba(255, 255, 255, 0.08);

      /* Borders & Dividers */
      --fluent-stroke-card: rgba(255, 255, 255, 0.08);
      --fluent-stroke-divider: rgba(255, 255, 255, 0.06);
      --fluent-stroke-control: rgba(255, 255, 255, 0.12);
      --fluent-stroke-focus: #60cdff;

      /* Typography & Text Brushes */
      --text-primary: #ffffff;
      --text-secondary: #d0d0d0;
      --text-tertiary: #909090;
      --text-disabled: #5c5c5c;

      /* Accent & Semantic Brand (Windows Fluent Blue & Status) */
      --accent-primary: #0078d4;
      --accent-hover: #1084d9;
      --accent-active: #006cbe;
      --accent-subtle: rgba(0, 120, 212, 0.15);
      --accent-border: rgba(96, 205, 255, 0.35);

      --status-safe: #6ccb5f;
      --status-safe-bg: rgba(108, 203, 95, 0.12);
      --status-safe-border: rgba(108, 203, 95, 0.3);

      --status-info: #60cdff;
      --status-info-bg: rgba(96, 205, 255, 0.12);
      --status-info-border: rgba(96, 205, 255, 0.3);

      --status-warn: #fce100;
      --status-warn-bg: rgba(252, 225, 0, 0.12);
      --status-warn-border: rgba(252, 225, 0, 0.3);

      --status-danger: #ff99a4;
      --status-danger-bg: rgba(255, 153, 164, 0.12);
      --status-danger-border: rgba(255, 153, 164, 0.3);

      --status-junction: #b4a0ff;
      --status-junction-bg: rgba(180, 160, 255, 0.12);
      --status-junction-border: rgba(180, 160, 255, 0.3);

      /* Radii & Controls */
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --radius-pill: 9999px;

      /* Font Family */
      --font-family: "Segoe UI Variable Text", "Segoe UI", -apple-system, BlinkMacSystemFont, "Microsoft YaHei", sans-serif;
      --font-mono: "Cascadia Code", "Consolas", monospace;

      /* Motion */
      --motion-timing: cubic-bezier(0.1, 0.9, 0.2, 1.0);
    }

    /* Reset & Base Layout */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-drag: none;
    }

    /* Windows 11 Native Custom Scrollbars */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.16);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.28);
    }

    body {
      font-family: var(--font-family);
      font-size: 13px;
      line-height: 1.5;
      color: var(--text-primary);
      background-color: var(--fluent-mica-base);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* SVG Icon Utility */
    .icon {
      width: 16px;
      height: 16px;
      fill: currentColor;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    /* ==========================================================================
       Window Titlebar & Shell
       ========================================================================== */
    .titlebar {
      height: 40px;
      background-color: var(--fluent-mica-alt);
      border-bottom: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      app-region: drag;
      z-index: 100;
      flex-shrink: 0;
    }

    .titlebar-brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .brand-logo-mark {
      width: 22px;
      height: 22px;
      border-radius: var(--radius-sm);
      background: linear-gradient(135deg, #0078d4 0%, #00bcbc 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba(0, 120, 212, 0.3);
    }

    .brand-logo-mark svg {
      width: 14px;
      height: 14px;
      fill: #ffffff;
    }

    .brand-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 0.2px;
    }

    .brand-badge {
      font-size: 10px;
      font-weight: 700;
      color: #60cdff;
      background: rgba(96, 205, 255, 0.15);
      border: 1px solid rgba(96, 205, 255, 0.3);
      padding: 1px 6px;
      border-radius: var(--radius-sm);
      text-transform: uppercase;
    }

    .titlebar-center {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .disk-selector-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      background-color: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-control);
      border-radius: var(--radius-pill);
      padding: 4px 12px;
      font-size: 12px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 120ms ease;
    }

    .disk-selector-pill:hover {
      background-color: var(--fluent-subtle-hover);
      color: var(--text-primary);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .titlebar-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .win-caption-btn {
      width: 32px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--radius-sm);
      background: transparent;
      border: none;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 100ms ease;
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
       App Layout: Sidebar (NavigationView) + Content Area
       ========================================================================== */
    .app-body {
      flex: 1;
      display: flex;
      overflow: hidden;
      background-color: var(--fluent-mica-base);
    }

    /* NavigationView Sidebar */
    .navigation-view {
      width: 236px;
      background-color: var(--fluent-mica-alt);
      border-right: 1px solid var(--fluent-stroke-divider);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 12px 8px;
      flex-shrink: 0;
      overflow-y: auto;
    }

    .nav-group-title {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-tertiary);
      padding: 6px 12px 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
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
      top: 6px;
      bottom: 6px;
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
    }

    .nav-item.active .nav-badge {
      background: var(--accent-subtle);
      color: #60cdff;
    }

    /* Sidebar Footer Disk Status */
    .sidebar-footer {
      background-color: var(--fluent-layer-base);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 12px;
      flex-shrink: 0;
    }

    .sidebar-footer-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11.5px;
    }

    .sidebar-disk-label {
      color: var(--text-secondary);
      font-weight: 600;
    }

    .sidebar-disk-free {
      color: var(--status-safe);
      font-family: var(--font-mono);
      font-size: 11px;
    }

    .sidebar-progress-track {
      height: 5px;
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-pill);
      overflow: hidden;
      display: flex;
    }

    .sidebar-progress-fill {
      background: linear-gradient(90deg, #0078d4, #60cdff);
      height: 100%;
      transition: width 300ms ease;
    }

    .sidebar-engine-tag {
      font-size: 10.5px;
      color: var(--text-tertiary);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* ==========================================================================
       Content Canvas & Workspaces
       ========================================================================== */
    .content-canvas {
      flex: 1;
      background-color: var(--fluent-layer-base);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }

    .workspace-pane {
      display: none;
      flex: 1;
      flex-direction: column;
      overflow-y: auto;
      padding: 24px 28px;
      gap: 20px;
    }

    .workspace-pane > * {
      flex-shrink: 0;
    }

    .workspace-pane.active {
      display: flex;
    }

    /* Header Bar within Workspace */
    .workspace-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      border-bottom: 1px solid var(--fluent-stroke-divider);
      padding-bottom: 16px;
    }

    .workspace-title-box h1 {
      font-size: 20px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 4px;
    }

    .workspace-title-box p {
      font-size: 12.5px;
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
      padding: 6px 14px;
      font-size: 12.5px;
      font-weight: 500;
      border-radius: var(--radius-sm);
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 120ms ease;
      text-decoration: none;
      white-space: nowrap;
    }

    .btn:active {
      transform: scale(0.985);
    }

    .btn-primary {
      background-color: var(--accent-primary);
      color: #ffffff;
      border-color: var(--accent-hover);
    }

    .btn-primary:hover {
      background-color: var(--accent-hover);
      box-shadow: 0 2px 8px rgba(0, 120, 212, 0.4);
    }

    .btn-secondary {
      background-color: var(--fluent-card-bg);
      color: var(--text-primary);
      border-color: var(--fluent-stroke-control);
    }

    .btn-secondary:hover {
      background-color: var(--fluent-card-hover);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .btn-success {
      background-color: #107c41;
      color: #ffffff;
    }

    .btn-success:hover {
      background-color: #138747;
    }

    .btn-danger {
      background-color: rgba(209, 52, 56, 0.2);
      color: var(--status-danger);
      border-color: var(--status-danger-border);
    }

    .btn-danger:hover {
      background-color: #d13438;
      color: #ffffff;
    }

    /* ==========================================================================
       HERO: Visual Storage Ribbon & Health Center (Spend boldness here)
       ========================================================================== */
    .storage-hero-card {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .hero-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .hero-metric-group {
      display: flex;
      align-items: baseline;
      gap: 10px;
    }

    .hero-metric-figure {
      font-size: 32px;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.5px;
      font-family: var(--font-family);
    }

    .hero-metric-unit {
      font-size: 18px;
      font-weight: 600;
      color: #60cdff;
    }

    .hero-metric-desc {
      font-size: 13px;
      color: var(--text-secondary);
    }

    /* Storage Allocation Strip */
    .storage-ribbon-container {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .storage-ribbon {
      height: 20px;
      background-color: rgba(0, 0, 0, 0.3);
      border-radius: var(--radius-sm);
      overflow: hidden;
      display: flex;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .ribbon-segment {
      height: 100%;
      transition: width 400ms var(--motion-timing);
      position: relative;
    }

    .seg-system { background-color: #4f52b2; }
    .seg-apps { background-color: #0078d4; }
    .seg-cleanable { background-color: #00b7c3; }
    .seg-migrate { background-color: #8764b8; }
    .seg-free { background-color: rgba(255, 255, 255, 0.1); }

    .ribbon-legend {
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 12px;
      color: var(--text-secondary);
      flex-wrap: wrap;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 2px;
    }

    /* Reclaimable Category Tiles */
    .reclaim-tiles-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
    }

    .reclaim-tile {
      background: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: border-color 150ms ease, background-color 150ms ease;
    }

    .reclaim-tile:hover {
      background: var(--fluent-subtle-hover);
      border-color: rgba(255, 255, 255, 0.16);
    }

    .tile-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: var(--text-tertiary);
      font-size: 11.5px;
    }

    .tile-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-primary);
    }

    .tile-size {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-primary);
      font-family: var(--font-family);
    }

    .tile-subtext {
      font-size: 11.5px;
      color: var(--text-secondary);
    }

    /* ==========================================================================
       Desktop CommandBar & Data Grid (CleanFlow Master-Detail)
       ========================================================================== */
    .desktop-commandbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background-color: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 8px 12px;
    }

    .commandbar-left {
      display: flex;
      align-items: center;
      gap: 8px;
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
      padding: 5px 10px 5px 28px;
      font-size: 12.5px;
      color: var(--text-primary);
      outline: none;
      width: 220px;
      transition: border-color 120ms ease;
    }

    .search-box input:focus {
      border-color: var(--fluent-stroke-focus);
      background-color: var(--fluent-layer-base);
    }

    .search-icon {
      position: absolute;
      left: 8px;
      color: var(--text-tertiary);
    }

    .filter-tabs {
      display: flex;
      align-items: center;
      gap: 2px;
      background: var(--fluent-subtle);
      padding: 2px;
      border-radius: var(--radius-sm);
    }

    .filter-tab {
      padding: 4px 10px;
      font-size: 12px;
      color: var(--text-secondary);
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 100ms ease;
    }

    .filter-tab.active {
      background-color: var(--fluent-card-bg);
      color: var(--text-primary);
      font-weight: 600;
    }

    /* Native-Styled Data Grid Table */
    .data-grid-container {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      overflow-x: auto;
      display: block;
      width: 100%;
    }

    .data-grid {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 12.5px;
    }

    .data-grid thead th {
      background-color: rgba(255, 255, 255, 0.03);
      border-bottom: 1px solid var(--fluent-stroke-divider);
      color: var(--text-tertiary);
      font-weight: 600;
      font-size: 11.5px;
      padding: 10px 14px;
      white-space: nowrap;
    }

    .data-grid tbody tr {
      border-bottom: 1px solid var(--fluent-stroke-divider);
      transition: background-color 100ms ease;
    }

    .data-grid tbody tr:nth-child(even) {
      background-color: rgba(255, 255, 255, 0.015);
    }

    .data-grid tbody tr:last-child {
      border-bottom: none;
    }

    .data-grid tbody tr:hover {
      background-color: var(--fluent-subtle-hover);
    }

    .data-grid td {
      padding: 10px 14px;
      vertical-align: middle;
      color: var(--text-secondary);
    }

    .data-grid td.td-name {
      color: var(--text-primary);
      font-weight: 500;
    }

    .col-checkbox {
      width: 38px;
      text-align: center;
    }

    /* Windows 11 Fluent Checkbox */
    input[type="checkbox"] {
      appearance: none;
      width: 16px;
      height: 16px;
      border: 1px solid var(--fluent-stroke-control);
      border-radius: 3px;
      background-color: var(--fluent-subtle);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      vertical-align: middle;
      position: relative;
      transition: all 100ms ease;
    }

    input[type="checkbox"]:checked {
      background-color: var(--accent-primary);
      border-color: var(--accent-primary);
    }

    input[type="checkbox"]:checked::after {
      content: "";
      width: 4px;
      height: 8px;
      border: solid #ffffff;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
      position: absolute;
      top: 1px;
    }

    /* Badges */
    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 8px;
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

    /* Inline action buttons */
    .table-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .icon-action-btn {
      width: 26px;
      height: 26px;
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

    /* ==========================================================================
       Junction Migration & Registry Studio UI
       ========================================================================== */
    .migration-banner {
      background: linear-gradient(135deg, rgba(135, 100, 184, 0.15) 0%, rgba(0, 120, 212, 0.15) 100%);
      border: 1px solid rgba(135, 100, 184, 0.3);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .migration-banner-text h3 {
      font-size: 14px;
      font-weight: 600;
      color: #ffffff;
      margin-bottom: 3px;
    }

    .migration-banner-text p {
      font-size: 12px;
      color: var(--text-secondary);
    }

    .custom-migrate-box {
      background: var(--fluent-card-bg);
      border: 1px solid var(--fluent-stroke-card);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .form-row {
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex: 1;
    }

    .form-group label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .form-control {
      background-color: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-control);
      border-radius: var(--radius-sm);
      padding: 7px 10px;
      font-size: 12.5px;
      color: var(--text-primary);
      outline: none;
      font-family: var(--font-mono);
      transition: border-color 120ms ease;
    }

    .form-control:focus {
      border-color: var(--fluent-stroke-focus);
      background-color: var(--fluent-layer-base);
    }

    select.form-control {
      font-family: var(--font-family);
      cursor: pointer;
    }

    /* Analysis feedback preview */
    .path-stats-feedback {
      background-color: var(--fluent-subtle);
      border: 1px solid var(--fluent-stroke-control);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      display: none;
      font-size: 12px;
      color: var(--text-secondary);
    }

    .path-stats-feedback.active {
      display: block;
    }

    /* Section Subheadings */
    .section-subheading {
      font-size: 13.5px;
      font-weight: 600;
      color: #ffffff;
      margin-top: 6px;
    }

    /* ==========================================================================
       Native WinUI 3 ContentDialog Modal
       ========================================================================== */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(16px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .modal-overlay.active {
      display: flex;
    }

    .content-dialog {
      width: 100%;
      max-width: 520px;
      background-color: #2b2b2b;
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: var(--radius-md);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: dialogPop 160ms var(--motion-timing);
    }

    @keyframes dialogPop {
      from { transform: scale(0.96); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .dialog-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .dialog-title {
      font-size: 15px;
      font-weight: 600;
      color: #ffffff;
    }

    .dialog-body {
      padding: 20px;
      font-size: 13px;
      color: var(--text-secondary);
      display: flex;
      flex-direction: column;
      gap: 14px;
      max-height: 60vh;
      overflow-y: auto;
    }

    .dialog-footer {
      padding: 14px 20px;
      background-color: rgba(0, 0, 0, 0.2);
      border-top: 1px solid var(--fluent-stroke-divider);
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
    }

    /* Modal Progress Indicators */
    .progress-bar-track {
      height: 6px;
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-pill);
      overflow: hidden;
    }

    .progress-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #0078d4, #00b7c3);
      width: 0%;
      transition: width 200ms ease;
    }

    /* Toast Notification */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 2000;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }

    .toast-message {
      background-color: #2e2e2e;
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: var(--radius-sm);
      padding: 10px 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 12.5px;
      color: #ffffff;
      animation: toastSlide 160ms var(--motion-timing);
      pointer-events: auto;
    }

    @keyframes toastSlide {
      from { transform: translateY(12px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
      * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body>

  <!-- Window Header / Titlebar -->
  <header class="titlebar">
    <div class="titlebar-brand">
      <div class="brand-logo-mark">
        <svg viewBox="0 0 24 24"><path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5zm0 2.18l7 3.89v4.93c0 4.61-3.12 8.91-7 10-3.88-1.09-7-5.39-7-10V8.07l7-3.89z"/></svg>
      </div>
      <span class="brand-title">CleanFlow Pro</span>
      <span class="brand-badge">v1.2</span>
    </div>

    <div class="titlebar-center">
      <div class="disk-selector-pill" id="currentDiskPill" onclick="refreshDisks()">
        <span class="icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm6-10H6V6h12v1z"/></svg>
        </span>
        <span id="diskSelectorLabel">系统盘 (C:)</span>
      </div>
    </div>

    <div class="titlebar-actions">
      <button class="win-caption-btn" title="最小化" onclick="minimizeWindow()">
        <svg class="icon" viewBox="0 0 24 24"><path d="M19 13H5v-2h14v2z"/></svg>
      </button>
      <button class="win-caption-btn" title="最大化" onclick="maximizeWindow()">
        <svg class="icon" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>
      </button>
      <button class="win-caption-btn btn-close" title="退出程序" onclick="shutdownApp()">
        <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/></svg>
      </button>
    </div>
  </header>

  <!-- App Body -->
  <div class="app-body">
    <!-- Fluent NavigationView Sidebar -->
    <nav class="navigation-view">
      <div class="nav-top-block">
        <div class="nav-group-title">核心空间治理</div>
        <ul class="nav-list">
          <li class="nav-item active" onclick="switchTab('overview')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg></span>
              <span>空间体检与清理</span>
            </div>
            <span class="nav-badge" id="badgeCleanable">--</span>
          </li>
          <li class="nav-item" onclick="switchTab('devcache')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg></span>
              <span>开发与编译缓存</span>
            </div>
            <span class="nav-badge" id="badgeDevCache">--</span>
          </li>
          <li class="nav-item" onclick="switchTab('browser')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg></span>
              <span>浏览器深度专清</span>
            </div>
            <span class="nav-badge" id="badgeBrowser">--</span>
          </li>
          <li class="nav-item" onclick="switchTab('registry')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-1 8h-3v3h-2v-3h-3v-2h3v-3h2v3h3v2z"/></svg></span>
              <span>注册表冗余修复</span>
            </div>
            <span class="nav-badge" id="badgeRegistry">扫描</span>
          </li>
          <li class="nav-item" onclick="switchTab('migration')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
              <span>目录无损搬家</span>
            </div>
            <span class="nav-badge" id="badgeMigrate">Junction</span>
          </li>
          <li class="nav-item" onclick="switchTab('giant')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
              <span>大文件雷达 (100M+)</span>
            </div>
            <span class="nav-badge" id="badgeGiantFiles">扫描</span>
          </li>
          <li class="nav-item" onclick="switchTab('vacuum')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 3C7.58 3 4 4.79 4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7c0-2.21-3.58-4-8-4zm0 2c3.87 0 6 1.5 6 2s-2.13 2-6 2-6-1.5-6-2 2.13-2 6-2zm6 12c0 .5-2.13 2-6 2s-6-1.5-6-2v-2.23c1.61.78 3.72 1.23 6 1.23s4.39-.45 6-1.23V17zm0-5c0 .5-2.13 2-6 2s-6-1.5-6-2v-2.23c1.61.78 3.72 1.23 6 1.23s4.39-.45 6-1.23V12z"/></svg></span>
              <span>数据库碎片收缩</span>
            </div>
            <span class="nav-badge" id="badgeVacuum">SQLite</span>
          </li>
        </ul>

        <div class="nav-group-title" style="margin-top: 14px;">高级定制</div>
        <ul class="nav-list">
          <li class="nav-item" onclick="switchTab('rules')">
            <div class="nav-item-left">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg></span>
              <span>自定义规则引擎</span>
            </div>
          </li>
        </ul>
      </div>

      <!-- Sidebar Footer Status -->
      <div class="sidebar-footer">
        <div class="sidebar-footer-top">
          <span class="sidebar-disk-label" id="sidebarDiskName">本地磁盘 (C:)</span>
          <span class="sidebar-disk-free" id="sidebarDiskFree">-- 可用</span>
        </div>
        <div class="sidebar-progress-track">
          <div class="sidebar-progress-fill" id="sidebarDiskFill" style="width: 80%;"></div>
        </div>
        <div class="sidebar-engine-tag">
          <span>Rust 原生内核</span>
          <span style="color: var(--status-safe);">运行正常</span>
        </div>
      </div>
    </nav>

    <!-- Main Workspaces Canvas -->
    <main class="content-canvas">

      <!-- ====================================================================
           WORKSPACE 1: Overview & Quick Clean
           ==================================================================== -->
      <section class="workspace-pane active" id="pane-overview">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>空间健康体检与清理</h1>
            <p>分析系统冗余、包管理器缓存及应用临时文件，精准安全回收存储</p>
          </div>
          <div class="workspace-controls">
            <button class="btn btn-secondary" onclick="runScan()">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
              <span>重新体检</span>
            </button>
            <button class="btn btn-primary" id="btnOneClickClean" onclick="executeCleanSelected()">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
              <span id="btnOneClickCleanLabel">立即一键清理</span>
            </button>
          </div>
        </div>

        <!-- HERO: Disk Capacity Ribbon & Metric -->
        <div class="storage-hero-card">
          <div class="hero-top-row">
            <div class="hero-metric-group">
              <div class="hero-metric-figure" id="heroCleanableFigure">0.0</div>
              <div class="hero-metric-unit" id="heroCleanableUnit">GB</div>
              <div class="hero-metric-desc" id="heroCleanableDesc">可安全释放空间</div>
            </div>
            <div class="badge-pill badge-safe" id="heroHealthBadge">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
              <span>建议立即清理</span>
            </div>
          </div>

          <div class="storage-ribbon-container">
            <div class="storage-ribbon">
              <div class="ribbon-segment seg-system" id="segSystem" style="width: 45%;" title="系统与常规数据"></div>
              <div class="ribbon-segment seg-apps" id="segApps" style="width: 25%;" title="已安装应用程序"></div>
              <div class="ribbon-segment seg-cleanable" id="segCleanable" style="width: 15%;" title="可清理缓存与临时文件"></div>
              <div class="ribbon-segment seg-free" id="segFree" style="width: 15%;" title="剩余空闲空间"></div>
            </div>
            <div class="ribbon-legend">
              <div class="legend-item"><div class="legend-dot seg-system"></div><span>系统与数据 (<span id="txtSystemSpace">--</span>)</span></div>
              <div class="legend-item"><div class="legend-dot seg-apps"></div><span>应用程序 (<span id="txtAppsSpace">--</span>)</span></div>
              <div class="legend-item"><div class="legend-dot seg-cleanable"></div><span>可清理缓存 (<span id="txtCleanableSpace">--</span>)</span></div>
              <div class="legend-item"><div class="legend-dot seg-free"></div><span>空闲空间 (<span id="txtFreeSpace">--</span>)</span></div>
            </div>
          </div>
        </div>

        <!-- Reclaimable Category Summary Tiles -->
        <div class="reclaim-tiles-grid">
          <div class="reclaim-tile">
            <div class="tile-header">
              <span>开发构建缓存</span>
              <span class="badge-pill badge-safe">100% 安全</span>
            </div>
            <div class="tile-size" id="tileDevSize">0 MB</div>
            <div class="tile-subtext">npm, pnpm, Unity, Gradle 等离线依赖包</div>
          </div>
          <div class="reclaim-tile">
            <div class="tile-header">
              <span>浏览器与网络缓存</span>
              <span class="badge-pill badge-safe">日常垃圾</span>
            </div>
            <div class="tile-size" id="tileBrowserSize">0 MB</div>
            <div class="tile-subtext">Edge、Chrome 离线页面与代码缓存</div>
          </div>
          <div class="reclaim-tile">
            <div class="tile-header">
              <span>系统与软件临时项</span>
              <span class="badge-pill badge-safe">安全</span>
            </div>
            <div class="tile-size" id="tileSysSize">0 MB</div>
            <div class="tile-subtext">Windows Temp, 缩略图, 飞书更新, 崩溃日志</div>
          </div>
          <div class="reclaim-tile">
            <div class="tile-header">
              <span>大资产迁移空间</span>
              <span class="badge-pill badge-junction">建议搬家</span>
            </div>
            <div class="tile-size" id="tileMigrateSize">0 MB</div>
            <div class="tile-subtext">Android 模拟器与微信数据，通过 Junction 搬迁</div>
          </div>
          <div class="reclaim-tile">
            <div class="tile-header">
              <span>数据库整理潜能</span>
              <span class="badge-pill badge-safe">无损压缩</span>
            </div>
            <div class="tile-size" id="tileDbSize">0 MB</div>
            <div class="tile-subtext">SQLite 空间收缩，释放 Freelist 碎片</div>
          </div>
        </div>

        <!-- CommandBar for Overview -->
        <div class="desktop-commandbar">
          <div class="commandbar-left">
            <div class="search-box">
              <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
              <input type="text" id="overviewSearchInput" placeholder="过滤项目或路径..." oninput="filterOverviewTable()">
            </div>
            <div class="filter-tabs">
              <div class="filter-tab active" onclick="setOverviewCategoryFilter('all', this)">全部</div>
              <div class="filter-tab" onclick="setOverviewCategoryFilter('browser', this)">浏览器缓存</div>
              <div class="filter-tab" onclick="setOverviewCategoryFilter('dev', this)">开发缓存</div>
              <div class="filter-tab" onclick="setOverviewCategoryFilter('system', this)">系统应用</div>
              <div class="filter-tab" onclick="setOverviewCategoryFilter('db', this)">数据库</div>
            </div>
          </div>
          <div>
            <span style="font-size: 12px; color: var(--text-tertiary);" id="tableItemCounter">已加载 0 个清理项目</span>
          </div>
        </div>

        <!-- Clean Items Table -->
        <div class="data-grid-container">
          <table class="data-grid">
            <thead>
              <tr>
                <th class="col-checkbox"><input type="checkbox" id="selectAllCheckbox" onchange="toggleSelectAll(this.checked)" checked></th>
                <th>清理项目</th>
                <th>分类</th>
                <th>目录 / 文件路径</th>
                <th style="text-align: right;">占用体积</th>
                <th>安全等级</th>
                <th style="text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody id="overviewTableBody">
              <tr>
                <td colspan="7" style="text-align: center; padding: 30px; color: var(--text-tertiary);">
                  正在加载清理清单...
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 2: Dev Stacks Cache
           ==================================================================== -->
      <section class="workspace-pane" id="pane-devcache">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>开发与编译缓存专项</h1>
            <p>管理构建时下载的包管理器包、IDE 沙箱及语言运行时离线缓存</p>
          </div>
          <div class="workspace-controls">
            <button class="btn btn-primary" onclick="cleanCategoryItems('dev_cache')">清理开发缓存</button>
          </div>
        </div>

        <div class="data-grid-container">
          <table class="data-grid">
            <thead>
              <tr>
                <th class="col-checkbox"><input type="checkbox" checked onchange="toggleDevAll(this.checked)"></th>
                <th>技术栈 / 工具</th>
                <th>路径说明</th>
                <th style="text-align: right;">占用大小</th>
                <th>文件数</th>
                <th style="text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody id="devTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 3: Browser Hygiene & Cache (NEW)
           ==================================================================== -->
      <section class="workspace-pane" id="pane-browser">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>主流浏览器深度专清</h1>
            <p>安全清理 Edge、Chrome、360 等浏览器的离线网页媒体与编译代码缓存，不影响历史记录、密码与书签</p>
          </div>
          <div class="workspace-controls">
            <button class="btn btn-primary" onclick="cleanCategoryItems('browser_cache')">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg></span>
              <span>一键清理浏览器缓存</span>
            </button>
          </div>
        </div>

        <div class="desktop-commandbar">
          <div class="commandbar-left">
            <div class="search-box">
              <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
              <input type="text" id="browserSearchInput" placeholder="按浏览器名称或路径过滤..." oninput="renderBrowserTable()">
            </div>
          </div>
          <div>
            <span style="font-size: 12px; color: var(--text-tertiary);" id="browserTableCounter">就绪</span>
          </div>
        </div>

        <div class="data-grid-container">
          <table class="data-grid">
            <thead>
              <tr>
                <th class="col-checkbox"><input type="checkbox" checked onchange="toggleBrowserAll(this.checked)"></th>
                <th>浏览器 / 缓存类型</th>
                <th>磁盘物理路径</th>
                <th style="text-align: right;">占用体积</th>
                <th>文件数</th>
                <th style="text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody id="browserTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 4: Registry Cleaner & Redundant Keys (NEW)
           ==================================================================== -->
      <section class="workspace-pane" id="pane-registry">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>注册表冗余与失效残留修复</h1>
            <p>智能排查已卸载软件的历史残留键、无效卸载项及失效 MUICache，修复前自动生成 .reg 可回滚备份</p>
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

        <div class="migration-banner" style="background: linear-gradient(135deg, rgba(0, 120, 212, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%); border-color: rgba(96, 205, 255, 0.3);">
          <div class="migration-banner-text">
            <h3>注册表无损安全机制</h3>
            <p>每次执行修复前，系统会自动在临时目录下生成标准 Windows .reg 格式备份文件。如需还原，只需双击备份文件即可完全回退。</p>
          </div>
          <button class="btn btn-secondary" onclick="openRegistryBackupFolder()">
            <span class="icon"><svg viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg></span>
            <span>浏览备份目录</span>
          </button>
        </div>

        <div class="desktop-commandbar">
          <div class="commandbar-left">
            <div class="search-box">
              <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
              <input type="text" id="registrySearchInput" placeholder="按路径或软件名过滤..." oninput="renderRegistryTable()">
            </div>
            <div class="filter-tabs">
              <div class="filter-tab active" onclick="setRegistryFilter('all', this)">全部</div>
              <div class="filter-tab" onclick="setRegistryFilter('mui', this)">应用缓存残留</div>
              <div class="filter-tab" onclick="setRegistryFilter('uninst', this)">卸载项残留</div>
            </div>
          </div>
          <div>
            <span style="font-size: 12px; color: var(--text-tertiary);" id="registryCounter">准备就绪</span>
          </div>
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
            <tbody id="registryTableBody">
              <tr>
                <td colspan="6" style="text-align: center; padding: 30px; color: var(--text-tertiary);">
                  正在扫描注册表失效项...
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 5: Junction Migration Studio
           ==================================================================== -->
      <section class="workspace-pane" id="pane-migration">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>目录无损搬家 (Junction 虚拟化)</h1>
            <p>将庞大资产搬迁至 D 盘或其它大容量驱动器，原位创建 NTFS Junction，软件无感照常运行</p>
          </div>
        </div>

        <div class="migration-banner">
          <div class="migration-banner-text">
            <h3>核心无损技术保障</h3>
            <p>底层采用 Windows NTFS 原生 Directory Junction 技术。搬迁完成后源目录化为虚拟联接点，应用访问路径完全保持不变。</p>
          </div>
          <button class="btn btn-secondary" onclick="loadActiveJunctions()">
            <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
            <span>刷新软链接</span>
          </button>
        </div>

        <!-- Custom Directory Migration Box -->
        <div class="custom-migrate-box">
          <h3 style="font-size: 13.5px; font-weight: 600; color: #ffffff;">自定义任意目录一键搬家</h3>
          <div class="form-row">
            <div class="form-group" style="flex: 3;">
              <label>需要搬迁的源目录绝对路径 (例如 C:\Users\EDY\.android\avd)</label>
              <input type="text" class="form-control" id="customMigrateSource" placeholder="输入或粘贴 C 盘目录路径...">
            </div>
            <div class="form-group" style="flex: 1;">
              <label>迁移目标盘符</label>
              <select class="form-control" id="customMigrateTargetDrive">
                <option value="D:">D 盘 (本地大容量磁盘)</option>
                <option value="E:">E 盘</option>
                <option value="F:">F 盘</option>
              </select>
            </div>
          </div>
          <div class="form-row" style="justify-content: flex-start; gap: 10px;">
            <button class="btn btn-secondary" onclick="analyzeCustomPath()">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg></span>
              <span>分析体积与进程占用</span>
            </button>
            <button class="btn btn-primary" id="btnStartCustomMigrate" onclick="startCustomPathMigration()" disabled>
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M16 13h-3V3h-2v10H8l4 4 4-4zM4 19v2h16v-2H4z"/></svg></span>
              <span>立即安全迁移并创建 Junction</span>
            </button>
          </div>
          <div class="path-stats-feedback" id="customPathFeedback"></div>
        </div>

        <!-- Preset Migration Recommendations -->
        <h3 class="section-subheading">系统检测到的高价值迁移项目</h3>
        <div class="data-grid-container">
          <table class="data-grid">
            <thead>
              <tr>
                <th>软件 / 资产名称</th>
                <th>当前原始路径</th>
                <th style="text-align: right;">体积</th>
                <th>状态</th>
                <th style="text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody id="presetMigrationTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>

        <!-- Active Migrated Junctions Table -->
        <h3 class="section-subheading">当前活动的 Junction 目录联接 (已迁移项)</h3>
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
            <tbody id="activeJunctionsTableBody">
              <tr>
                <td colspan="4" style="text-align: center; padding: 24px; color: var(--text-tertiary);">
                  暂无活动 Junction 记录
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 6: Giant Files Radar
           ==================================================================== -->
      <section class="workspace-pane" id="pane-giant">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>大文件雷达 (100MB+ 沉淀文件)</h1>
            <p>快速排查深层隐蔽的大型压缩包、系统镜像、历史废弃安装包</p>
          </div>
          <div class="workspace-controls">
            <button class="btn btn-secondary" onclick="loadGiantFiles()">
              <span class="icon"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></span>
              <span>刷新大文件</span>
            </button>
          </div>
        </div>

        <div class="desktop-commandbar">
          <div class="commandbar-left">
            <div class="search-box">
              <span class="icon search-icon"><svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></span>
              <input type="text" id="giantSearchInput" placeholder="按文件名或后缀过滤..." oninput="filterGiantTable()">
            </div>
            <div class="filter-tabs">
              <div class="filter-tab active" onclick="setGiantFilter('all', this)">全部</div>
              <div class="filter-tab" onclick="setGiantFilter('Archive', this)">压缩包</div>
              <div class="filter-tab" onclick="setGiantFilter('Executable', this)">安装包</div>
              <div class="filter-tab" onclick="setGiantFilter('Database', this)">数据库</div>
            </div>
          </div>
          <div>
            <span style="font-size: 12px; color: var(--text-tertiary);" id="giantFilesCounter">扫描就绪</span>
          </div>
        </div>

        <div class="data-grid-container">
          <table class="data-grid">
            <thead>
              <tr>
                <th>文件名称</th>
                <th>文件类型</th>
                <th>完整路径</th>
                <th style="text-align: right;">文件大小</th>
                <th style="text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody id="giantTableBody">
              <tr>
                <td colspan="5" style="text-align: center; padding: 40px; color: var(--text-tertiary);">
                  点击上方“刷新大文件”开始扫描 C 盘 100MB 以上大文件
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 7: Database Vacuum (SQLite)
           ==================================================================== -->
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
                <th>数据库物理路径</th>
                <th style="text-align: right;">当前文件大小</th>
                <th>技术特性</th>
                <th style="text-align: center;">操作</th>
              </tr>
            </thead>
            <tbody id="vacuumTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </section>

      <!-- ====================================================================
           WORKSPACE 8: Custom Rules Studio
           ==================================================================== -->
      <section class="workspace-pane" id="pane-rules">
        <div class="workspace-header">
          <div class="workspace-title-box">
            <h1>自定义规则引擎</h1>
            <p>配置用户专属的项目构建缓存与特定临时目录匹配规则</p>
          </div>
        </div>

        <div class="custom-migrate-box">
          <h3 style="font-size: 13.5px; font-weight: 600; color: #ffffff;">添加新清理规则</h3>
          <div class="form-row">
            <div class="form-group" style="flex: 1;">
              <label>规则友好名称 (例如: 我的项目临时产物)</label>
              <input type="text" class="form-control" id="customRuleName" placeholder="例如: Webpack dist 缓存">
            </div>
            <div class="form-group" style="flex: 2;">
              <label>匹配路径模式 (支持环境通配符)</label>
              <input type="text" class="form-control" id="customRulePattern" placeholder="例如: %LOCALAPPDATA%\MyTool\cache">
            </div>
          </div>
          <div class="form-row" style="justify-content: flex-start;">
            <button class="btn btn-primary" onclick="submitCustomRule()">保存规则并生效</button>
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- WinUI 3 ContentDialog: Migration Progress Modal -->
  <div class="modal-overlay" id="migrationModal">
    <div class="content-dialog">
      <div class="dialog-header">
        <span class="dialog-title" id="migrationModalTitle">正在搬家迁移中...</span>
      </div>
      <div class="dialog-body">
        <p id="migrationModalStatusText">正在复制数据文件到目标磁盘，请勿关闭程序...</p>
        <div class="progress-bar-track">
          <div class="progress-bar-fill" id="migrationProgressBar"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 11.5px; color: var(--text-tertiary);">
          <span id="migrationProgressPercent">0%</span>
          <span id="migrationTransferredBytes">0 MB / 0 MB</span>
        </div>
        <p class="path-text" id="migrationCurrentFileName" style="max-width: 100%;">准备中...</p>
      </div>
      <div class="dialog-footer" id="migrationModalFooter">
        <button class="btn btn-secondary" id="btnCancelMigration" onclick="closeMigrationModal()">关闭窗口</button>
      </div>
    </div>
  </div>

  <!-- WinUI 3 ContentDialog: General Confirmation Modal -->
  <div class="modal-overlay" id="confirmModal">
    <div class="content-dialog">
      <div class="dialog-header">
        <span class="dialog-title" id="confirmModalTitle">操作确认</span>
      </div>
      <div class="dialog-body" id="confirmModalBody">
        确定要执行此操作吗？
      </div>
      <div class="dialog-footer">
        <button class="btn btn-secondary" onclick="closeConfirmModal()">取消</button>
        <button class="btn btn-primary" id="confirmModalBtnAction">确认执行</button>
      </div>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Client-Side Runtime Engine -->
  <script>
    // State Store
    const state = {
      activeTab: 'overview',
      disks: [],
      scanReport: null,
      selectedPaths: new Set(),
      registryIssues: [],
      selectedRegistryIds: new Set(),
      giantFiles: [],
      activeJunctions: [],
      overviewFilterCategory: 'all',
      overviewSearchTerm: '',
      registryFilterCategory: 'all',
      giantFilterCategory: 'all',
      giantSearchTerm: '',
      migrationPollTimer: null
    };

    // Format Bytes utility
    function formatBytes(bytes) {
      if (bytes === undefined || bytes === null || isNaN(bytes)) return '0 B';
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i];
    }

    // Toast utility
    function showToast(text, duration = 3000) {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = 'toast-message';
      toast.innerHTML = `
        <span class="icon" style="color: #60cdff;"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>
        <span>${escapeHtml(text)}</span>
      `;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 200ms ease';
        setTimeout(() => toast.remove(), 200);
      }, duration);
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    // Tab Navigation
    function switchTab(tabId) {
      state.activeTab = tabId;
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.workspace-pane').forEach(el => el.classList.remove('active'));

      const targetPane = document.getElementById('pane-' + tabId);
      if (targetPane) targetPane.classList.add('active');

      // Highlight active nav item
      const navItems = document.querySelectorAll('.nav-item');
      if (tabId === 'overview') navItems[0].classList.add('active');
      else if (tabId === 'devcache') navItems[1].classList.add('active');
      else if (tabId === 'browser') { navItems[2].classList.add('active'); renderBrowserTable(); }
      else if (tabId === 'registry') { navItems[3].classList.add('active'); if (state.registryIssues.length === 0) loadRegistryIssues(); }
      else if (tabId === 'migration') { navItems[4].classList.add('active'); loadActiveJunctions(); renderPresetMigrationTable(); }
      else if (tabId === 'giant') { navItems[5].classList.add('active'); if (state.giantFiles.length === 0) loadGiantFiles(); }
      else if (tabId === 'vacuum') { navItems[6].classList.add('active'); }
      else if (tabId === 'rules') { navItems[7].classList.add('active'); }
    }

    // Refresh Disks
    async function refreshDisks() {
      try {
        const res = await fetch('/api/disks');
        if (!res.ok) throw new Error('网络请求失败');
        state.disks = await res.json();
        renderDisks();
      } catch (e) {
        showToast('读取磁盘失败: ' + e.message);
      }
    }

    function renderDisks() {
      if (!state.disks || state.disks.length === 0) return;
      const cDisk = state.disks.find(d => d.letter.toUpperCase().startsWith('C')) || state.disks[0];
      
      const totalGB = (cDisk.total_bytes / (1024**3)).toFixed(0);
      const freeGB = (cDisk.free_bytes / (1024**3)).toFixed(1);
      const usedGB = (cDisk.used_bytes / (1024**3)).toFixed(1);

      document.getElementById('diskSelectorLabel').innerText = `${cDisk.letter} 盘 (可用 ${freeGB} GB / ${totalGB} GB)`;
      document.getElementById('sidebarDiskName').innerText = `本地磁盘 (${cDisk.letter})`;
      document.getElementById('sidebarDiskFree').innerText = `${freeGB} GB 可用`;
      document.getElementById('sidebarDiskFill').style.width = `${cDisk.usage_percent}%`;

      document.getElementById('txtFreeSpace').innerText = `${freeGB} GB`;
      
      updateStorageRibbon();
    }

    // Update Storage Ribbon Breakdown
    function updateStorageRibbon() {
      const cDisk = state.disks.find(d => d.letter.toUpperCase().startsWith('C')) || state.disks[0];
      if (!cDisk) return;

      const total = cDisk.total_bytes;
      const free = cDisk.free_bytes;
      let cleanable = 0;

      if (state.scanReport && state.scanReport.categories) {
        state.scanReport.categories.forEach(cat => {
          if (cat.id !== 'migration_targets') {
            cleanable += cat.total_size_bytes || 0;
          }
        });
      }

      const cleanablePct = Math.min(30, (cleanable / total) * 100);
      const freePct = (free / total) * 100;
      const systemPct = 35;
      const appsPct = Math.max(5, 100 - freePct - cleanablePct - systemPct);

      document.getElementById('segSystem').style.width = systemPct + '%';
      document.getElementById('segApps').style.width = appsPct + '%';
      document.getElementById('segCleanable').style.width = cleanablePct + '%';
      document.getElementById('segFree').style.width = freePct + '%';

      document.getElementById('txtSystemSpace').innerText = '系统基础';
      document.getElementById('txtAppsSpace').innerText = '已装应用';
      document.getElementById('txtCleanableSpace').innerText = formatBytes(cleanable);
    }

    // Run Full Scan
    async function runScan() {
      showToast('正在快速体检 C 盘存储与系统缓存...');
      document.getElementById('btnOneClickClean').disabled = true;
      document.getElementById('overviewTableBody').innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-secondary);">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
              <span class="icon" style="color: #60cdff; transform: scale(1.5);"><svg viewBox="0 0 24 24"><path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"/></svg></span>
              <span>正在深度索引浏览器缓存、开发包及系统临时项...</span>
            </div>
          </td>
        </tr>
      `;

      try {
        const res = await fetch('/api/scan');
        if (!res.ok) throw new Error('扫描失败');
        state.scanReport = await res.json();
        
        // Reset selections
        state.selectedPaths.clear();
        state.scanReport.categories.forEach(cat => {
          if (cat.id !== 'migration_targets') {
            cat.rules.forEach(rule => {
              if (rule.default_checked) {
                rule.matched_paths.forEach(mp => {
                  if (mp.size_bytes > 0) state.selectedPaths.add(mp.path);
                });
              }
            });
          }
        });

        renderOverviewTable();
        renderDevCacheTable();
        renderBrowserTable();
        renderVacuumTable();
        renderPresetMigrationTable();
        updateOverviewMetrics();
        updateStorageRibbon();
        loadRegistryIssues();
        showToast('体检完成，已定位可释放空间');
      } catch (e) {
        showToast('扫描发生错误: ' + e.message);
      } finally {
        document.getElementById('btnOneClickClean').disabled = false;
      }
    }

    // Update Overview Metrics & Tiles
    function updateOverviewMetrics() {
      if (!state.scanReport || !state.scanReport.categories) return;

      let devTotal = 0;
      let browserTotal = 0;
      let sysTotal = 0;
      let migrateTotal = 0;
      let dbTotal = 0;
      let cleanableTotal = 0;

      state.scanReport.categories.forEach(cat => {
        if (cat.id === 'dev_cache') devTotal += cat.total_size_bytes;
        else if (cat.id === 'browser_cache') browserTotal += cat.total_size_bytes;
        else if (cat.id === 'sys_temp' || cat.id === 'office_chat' || cat.id === 'ai_tools') sysTotal += cat.total_size_bytes;
        else if (cat.id === 'migration_targets') migrateTotal += cat.total_size_bytes;
        else if (cat.id === 'sqlite_optimize') dbTotal += cat.total_size_bytes;
      });

      cleanableTotal = devTotal + browserTotal + sysTotal + dbTotal;

      const cleanableGB = (cleanableTotal / (1024**3)).toFixed(1);
      document.getElementById('heroCleanableFigure').innerText = cleanableGB;
      document.getElementById('heroCleanableDesc').innerText = `已就绪 ${formatBytes(cleanableTotal)}，包含浏览器、开发包与临时垃圾`;
      document.getElementById('btnOneClickCleanLabel').innerText = `一键快速清理 (${formatBytes(cleanableTotal)})`;

      document.getElementById('badgeCleanable').innerText = formatBytes(cleanableTotal);
      document.getElementById('badgeDevCache').innerText = formatBytes(devTotal);
      document.getElementById('badgeBrowser').innerText = formatBytes(browserTotal);

      document.getElementById('tileDevSize').innerText = formatBytes(devTotal);
      document.getElementById('tileBrowserSize').innerText = formatBytes(browserTotal);
      document.getElementById('tileSysSize').innerText = formatBytes(sysTotal);
      document.getElementById('tileMigrateSize').innerText = formatBytes(migrateTotal);
      document.getElementById('tileDbSize').innerText = formatBytes(dbTotal);
    }

    // Render Overview Table
    function renderOverviewTable() {
      const tbody = document.getElementById('overviewTableBody');
      tbody.innerHTML = '';

      if (!state.scanReport || !state.scanReport.categories) return;

      let allMatchedItems = [];
      state.scanReport.categories.forEach(cat => {
        if (cat.id === 'migration_targets') return; // Handled in migration studio

        cat.rules.forEach(rule => {
          rule.matched_paths.forEach(mp => {
            allMatchedItems.push({
              ruleName: rule.name,
              categoryId: cat.id,
              categoryName: cat.name,
              path: mp.path,
              size_bytes: mp.size_bytes,
              file_count: mp.file_count,
              is_dir: mp.is_dir,
              risk: cat.risk_level
            });
          });
        });
      });

      // Filter by search and tab
      const filtered = allMatchedItems.filter(item => {
        if (state.overviewFilterCategory === 'browser' && item.categoryId !== 'browser_cache') return false;
        if (state.overviewFilterCategory === 'dev' && item.categoryId !== 'dev_cache') return false;
        if (state.overviewFilterCategory === 'system' && item.categoryId !== 'sys_temp' && item.categoryId !== 'office_chat') return false;
        if (state.overviewFilterCategory === 'db' && item.categoryId !== 'sqlite_optimize') return false;

        if (state.overviewSearchTerm) {
          const q = state.overviewSearchTerm.toLowerCase();
          return item.ruleName.toLowerCase().includes(q) || item.path.toLowerCase().includes(q);
        }
        return true;
      });

      document.getElementById('tableItemCounter').innerText = `显示 ${filtered.length} 个清理项目`;

      if (filtered.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="7" style="text-align: center; padding: 30px; color: var(--text-tertiary);">
              未发现匹配的清理项或已完全释放
            </td>
          </tr>
        `;
        return;
      }

      filtered.forEach(item => {
        const tr = document.createElement('tr');
        const isChecked = state.selectedPaths.has(item.path);

        let badgeClass = 'badge-safe';
        let badgeText = '安全清理';
        if (item.categoryId === 'sqlite_optimize') {
          badgeClass = 'badge-safe';
          badgeText = '无损收缩';
        } else if (item.risk === 'medium') {
          badgeClass = 'badge-warn';
          badgeText = '推荐保留';
        }

        tr.innerHTML = `
          <td class="col-checkbox">
            <input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleItemSelection('${escapeHtml(item.path)}', this.checked)">
          </td>
          <td class="td-name">${escapeHtml(item.ruleName)}</td>
          <td><span style="font-size: 11.5px; color: var(--text-secondary);">${escapeHtml(item.categoryName)}</span></td>
          <td><span class="path-text" title="${escapeHtml(item.path)}">${escapeHtml(item.path)}</span></td>
          <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #ffffff;">
            ${formatBytes(item.size_bytes)}
          </td>
          <td><span class="badge-pill ${badgeClass}">${badgeText}</span></td>
          <td style="text-align: center;">
            <div class="table-actions" style="justify-content: center;">
              <button class="icon-action-btn" title="在资源管理器中打开" onclick="revealInExplorer('${escapeHtml(item.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
              </button>
              <button class="icon-action-btn" title="立即单独清理" onclick="cleanSinglePath('${escapeHtml(item.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12z"/></svg>
              </button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Toggle Item Selection
    function toggleItemSelection(path, checked) {
      if (checked) state.selectedPaths.add(path);
      else state.selectedPaths.delete(path);
      updateSelectedButtonLabel();
    }

    function toggleSelectAll(checked) {
      state.selectedPaths.clear();
      if (checked && state.scanReport && state.scanReport.categories) {
        state.scanReport.categories.forEach(cat => {
          if (cat.id !== 'migration_targets') {
            cat.rules.forEach(rule => {
              rule.matched_paths.forEach(mp => {
                if (mp.size_bytes > 0) state.selectedPaths.add(mp.path);
              });
            });
          }
        });
      }
      renderOverviewTable();
      updateSelectedButtonLabel();
    }

    function updateSelectedButtonLabel() {
      let selectedBytes = 0;
      if (state.scanReport) {
        state.scanReport.categories.forEach(cat => {
          cat.rules.forEach(r => {
            r.matched_paths.forEach(mp => {
              if (state.selectedPaths.has(mp.path)) selectedBytes += mp.size_bytes;
            });
          });
        });
      }
      document.getElementById('btnOneClickCleanLabel').innerText = `清理选中项 (${formatBytes(selectedBytes)})`;
    }

    function setOverviewCategoryFilter(cat, el) {
      state.overviewFilterCategory = cat;
      document.querySelectorAll('#pane-overview .filter-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderOverviewTable();
    }

    function filterOverviewTable() {
      state.overviewSearchTerm = document.getElementById('overviewSearchInput').value;
      renderOverviewTable();
    }

    // Clean Category Items Helper
    function cleanCategoryItems(catId) {
      const pathsToClean = [];
      if (state.scanReport) {
        const cat = state.scanReport.categories.find(c => c.id === catId);
        if (cat) {
          cat.rules.forEach(r => {
            r.matched_paths.forEach(mp => {
              if (mp.size_bytes > 0) pathsToClean.push(mp.path);
            });
          });
        }
      }

      if (pathsToClean.length === 0) {
        showToast('当前分类暂无可清理项目');
        return;
      }

      openConfirmModal(
        '专项清理确认',
        `即将清理该分类下的 ${pathsToClean.length} 个缓存目录，确认继续吗？`,
        async () => {
          closeConfirmModal();
          showToast('正在清理...');
          try {
            const res = await fetch('/api/clean', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ paths: pathsToClean })
            });
            const data = await res.json();
            if (data.success) {
              showToast(`清理成功，释放 ${formatBytes(data.bytes_freed)}`);
              runScan();
              refreshDisks();
            }
          } catch (e) {
            showToast('请求异常: ' + e.message);
          }
        }
      );
    }

    // Execute Clean Selected
    function executeCleanSelected() {
      if (state.selectedPaths.size === 0) {
        showToast('请先勾选需要清理的项目');
        return;
      }

      openConfirmModal(
        '清理确认',
        `即将安全删除选中的 ${state.selectedPaths.size} 个清理目录与临时文件。所有规则均已经过严谨安全性校验，不会破坏正在运行的系统核心。`,
        async () => {
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
              showToast(`清理圆满完成！成功释放 ${formatBytes(data.bytes_freed)} 空间`);
              runScan();
              refreshDisks();
            } else {
              showToast('清理遇到异常: ' + (data.errors ? data.errors.join('; ') : '未知错误'));
            }
          } catch (e) {
            showToast('清理请求失败: ' + e.message);
          }
        }
      );
    }

    // Clean Single Path
    function cleanSinglePath(path) {
      openConfirmModal(
        '单独清理确认',
        `确定要清理以下路径内容吗？<br><br><span class="path-text" style="color:#ffffff;">${escapeHtml(path)}</span>`,
        async () => {
          closeConfirmModal();
          showToast('正在清理...');
          try {
            const res = await fetch('/api/clean', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ paths: [path] })
            });
            const data = await res.json();
            if (data.success) {
              showToast(`成功释放 ${formatBytes(data.bytes_freed)}`);
              runScan();
              refreshDisks();
            }
          } catch (e) {
            showToast('清理失败: ' + e.message);
          }
        }
      );
    }

    // Reveal in Windows Explorer
    async function revealInExplorer(path) {
      try {
        await fetch('/api/reveal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: path })
        });
        showToast('已在 Windows 文件资源管理器中定位');
      } catch (e) {
        showToast('打开失败: ' + e.message);
      }
    }

    // ========================================================================
    // Browser Hygiene Table (NEW)
    // ========================================================================
    function renderBrowserTable() {
      const tbody = document.getElementById('browserTableBody');
      tbody.innerHTML = '';
      if (!state.scanReport) return;

      const browserCat = state.scanReport.categories.find(c => c.id === 'browser_cache');
      if (!browserCat || !browserCat.rules) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 24px; color: var(--text-tertiary);">暂无浏览器缓存记录</td></tr>`;
        return;
      }

      const q = (document.getElementById('browserSearchInput')?.value || '').toLowerCase();
      let matchedCount = 0;

      browserCat.rules.forEach(rule => {
        rule.matched_paths.forEach(mp => {
          if (q && !rule.name.toLowerCase().includes(q) && !mp.path.toLowerCase().includes(q)) return;
          matchedCount++;
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked></td>
            <td class="td-name">${escapeHtml(rule.name)}</td>
            <td><span class="path-text">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #ffffff;">${formatBytes(mp.size_bytes)}</td>
            <td style="color: var(--text-tertiary);">${mp.file_count} 文件</td>
            <td style="text-align: center;">
              <div class="table-actions" style="justify-content: center;">
                <button class="icon-action-btn" title="定位目录" onclick="revealInExplorer('${escapeHtml(mp.path)}')">
                  <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
                </button>
                <button class="btn btn-secondary" style="padding: 3px 8px; font-size: 11px;" onclick="cleanSinglePath('${escapeHtml(mp.path)}')">清理</button>
              </div>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });

      document.getElementById('browserTableCounter').innerText = `已检测到 ${matchedCount} 处浏览器缓存`;
    }

    function toggleBrowserAll(checked) {
      document.querySelectorAll('#browserTableBody input[type="checkbox"]').forEach(c => c.checked = checked);
    }

    // ========================================================================
    // Registry Cleaner (NEW)
    // ========================================================================
    async function loadRegistryIssues() {
      document.getElementById('registryTableBody').innerHTML = `
        <tr><td colspan="6" style="text-align: center; padding: 30px; color: var(--text-secondary);">正在深度排查无效卸载信息与死链应用缓存...</td></tr>
      `;
      try {
        const res = await fetch('/api/registry/scan');
        if (!res.ok) throw new Error('扫描注册表失败');
        state.registryIssues = await res.json();
        state.selectedRegistryIds = new Set(state.registryIssues.map(i => i.id));
        document.getElementById('badgeRegistry').innerText = state.registryIssues.length;
        renderRegistryTable();
      } catch (e) {
        showToast('读取注册表失败: ' + e.message);
      }
    }

    function renderRegistryTable() {
      const tbody = document.getElementById('registryTableBody');
      tbody.innerHTML = '';

      const q = (document.getElementById('registrySearchInput')?.value || '').toLowerCase();

      const filtered = state.registryIssues.filter(item => {
        if (state.registryFilterCategory === 'mui' && !item.category.includes('MUICache')) return false;
        if (state.registryFilterCategory === 'uninst' && !item.category.includes('Uninstall')) return false;
        if (q) {
          return item.invalid_path.toLowerCase().includes(q) || item.category.toLowerCase().includes(q);
        }
        return true;
      });

      document.getElementById('registryCounter').innerText = `发现 ${filtered.length} 处冗余项目`;
      document.getElementById('btnCleanRegistryLabel').innerText = `一键安全修复 (${state.selectedRegistryIds.size} 项)`;

      if (filtered.length === 0) {
        tbody.innerHTML = `
          <tr><td colspan="6" style="text-align: center; padding: 30px; color: var(--text-tertiary);">未发现注册表失效项目，系统配置健康干净</td></tr>
        `;
        return;
      }

      filtered.forEach(item => {
        const tr = document.createElement('tr');
        const isChecked = state.selectedRegistryIds.has(item.id);

        tr.innerHTML = `
          <td class="col-checkbox">
            <input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleRegistryItem('${item.id}', this.checked)">
          </td>
          <td class="td-name"><span class="badge-pill badge-warn">${escapeHtml(item.category)}</span></td>
          <td><span class="path-text" title="${escapeHtml(item.invalid_path)}" style="color: #ff99a4;">${escapeHtml(item.invalid_path)}</span></td>
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
      if (checked) {
        state.registryIssues.forEach(i => state.selectedRegistryIds.add(i.id));
      }
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

      openConfirmModal(
        '注册表修复确认',
        `即将安全修复选中的 ${state.selectedRegistryIds.size} 个无效注册表残留条目。<br><br><strong>系统将自动在修复前导出 .reg 完整回滚备份</strong>，确保 100% 安全无后顾之忧。`,
        async () => {
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
              showToast('部分项目处理遇到错误: ' + (data.errors ? data.errors.join('; ') : '未知错误'));
            }
          } catch (e) {
            showToast('请求异常: ' + e.message);
          }
        }
      );
    }

    function cleanSingleRegistryItem(id) {
      fetch('/api/registry/clean', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: [id] })
      }).then(r => r.json()).then(data => {
        showToast('已修复该项');
        loadRegistryIssues();
      });
    }

    function openRegistryBackupFolder() {
      fetch('/api/reveal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: 'C:\\Users\\EDY\\AppData\\Local\\Temp\\cleanflow_registry_backups' })
      }).then(() => showToast('已在资源管理器中打开备份文件夹'));
    }

    // ========================================================================
    // Dev Stacks Table
    // ========================================================================
    function renderDevCacheTable() {
      const tbody = document.getElementById('devTableBody');
      tbody.innerHTML = '';
      if (!state.scanReport) return;

      const devCat = state.scanReport.categories.find(c => c.id === 'dev_cache');
      if (!devCat || !devCat.rules) return;

      devCat.rules.forEach(rule => {
        rule.matched_paths.forEach(mp => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td class="col-checkbox"><input type="checkbox" checked></td>
            <td class="td-name">${escapeHtml(rule.name)}</td>
            <td><span class="path-text">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #ffffff;">${formatBytes(mp.size_bytes)}</td>
            <td style="color: var(--text-tertiary);">${mp.file_count} 文件</td>
            <td style="text-align: center;">
              <button class="btn btn-secondary" style="padding: 3px 8px; font-size: 11.5px;" onclick="cleanSinglePath('${escapeHtml(mp.path)}')">清理</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    // ========================================================================
    // Database Vacuum Table
    // ========================================================================
    function renderVacuumTable() {
      const tbody = document.getElementById('vacuumTableBody');
      tbody.innerHTML = '';
      if (!state.scanReport) return;

      const dbCat = state.scanReport.categories.find(c => c.id === 'sqlite_optimize');
      if (!dbCat || !dbCat.rules) return;

      dbCat.rules.forEach(rule => {
        rule.matched_paths.forEach(mp => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td class="td-name">${escapeHtml(rule.name)}</td>
            <td><span class="path-text">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #ffffff;">${formatBytes(mp.size_bytes)}</td>
            <td><span class="badge-pill badge-safe">无损 VACUUM</span></td>
            <td style="text-align: center;">
              <button class="btn btn-primary" style="padding: 3px 10px; font-size: 11.5px;" onclick="executeVacuum('${escapeHtml(mp.path)}')">收缩碎片</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    async function executeVacuum(dbPath) {
      showToast('正在执行 SQLite VACUUM 碎片无损收缩...');
      try {
        const res = await fetch('/api/vacuum', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ db_path: dbPath })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`数据库优化完毕！成功收缩释放 ${formatBytes(data.bytes_freed)} 空间`);
          runScan();
        } else {
          showToast('收缩失败: ' + (data.error || '未知错误'));
        }
      } catch (e) {
        showToast('请求异常: ' + e.message);
      }
    }

    // ========================================================================
    // Junction Migration Studio
    // ========================================================================
    function renderPresetMigrationTable() {
      const tbody = document.getElementById('presetMigrationTableBody');
      tbody.innerHTML = '';
      if (!state.scanReport) return;

      const migCat = state.scanReport.categories.find(c => c.id === 'migration_targets');
      if (!migCat || !migCat.rules) return;

      migCat.rules.forEach(rule => {
        rule.matched_paths.forEach(mp => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td class="td-name">${escapeHtml(rule.name)}</td>
            <td><span class="path-text">${escapeHtml(mp.path)}</span></td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #ffffff;">${formatBytes(mp.size_bytes)}</td>
            <td><span class="badge-pill badge-junction">建议迁移至 D 盘</span></td>
            <td style="text-align: center;">
              <button class="btn btn-primary" style="padding: 3px 12px; font-size: 11.5px;" onclick="triggerPresetMigration('${escapeHtml(mp.path)}')">一键搬家</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      });
    }

    async function loadActiveJunctions() {
      try {
        const res = await fetch('/api/junctions');
        if (!res.ok) throw new Error('读取 Junctions 失败');
        state.activeJunctions = await res.json();
        renderActiveJunctions();
      } catch (e) {
        showToast('读取活动软链接失败: ' + e.message);
      }
    }

    function renderActiveJunctions() {
      const tbody = document.getElementById('activeJunctionsTableBody');
      tbody.innerHTML = '';

      if (!state.activeJunctions || state.activeJunctions.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="4" style="text-align: center; padding: 24px; color: var(--text-tertiary);">
              当前暂无活动的迁移软链接
            </td>
          </tr>
        `;
        return;
      }

      state.activeJunctions.forEach(j => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="td-name"><span class="path-text">${escapeHtml(j.original_path)}</span></td>
          <td><span class="path-text" style="color: #60cdff;">${escapeHtml(j.target_path)}</span></td>
          <td style="font-size: 11.5px; color: var(--text-tertiary);">${escapeHtml(j.created_at || '已生效')}</td>
          <td style="text-align: center;">
            <div class="table-actions" style="justify-content: center;">
              <button class="btn btn-secondary" style="padding: 3px 8px; font-size: 11px;" onclick="revealInExplorer('${escapeHtml(j.target_path)}')">打开目标</button>
              <button class="btn btn-danger" style="padding: 3px 8px; font-size: 11px;" onclick="rollbackJunction('${escapeHtml(j.original_path)}')">还原回 C 盘</button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Rollback Junction
    function rollbackJunction(sourcePath) {
      openConfirmModal(
        '还原软链接确认',
        `即将把位于大容量驱动器的数据搬迁回原 C 盘，并彻底删除系统 Junction 软链接：<br><br><span class="path-text" style="color:#ffffff;">${escapeHtml(sourcePath)}</span>`,
        async () => {
          closeConfirmModal();
          showToast('正在还原数据回 C 盘...');
          try {
            const res = await fetch('/api/junctions/rollback', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ source_path: sourcePath })
            });
            const data = await res.json();
            if (data.success) {
              showToast(`成功恢复回 C 盘并移除 Junction (${formatBytes(data.bytes_restored)})`);
              loadActiveJunctions();
              runScan();
              refreshDisks();
            } else {
              showToast('还原遇到错误: ' + (data.error || '未知失败'));
            }
          } catch (e) {
            showToast('请求异常: ' + e.message);
          }
        }
      );
    }

    // Analyze Custom Migration Path
    async function analyzeCustomPath() {
      const pathInput = document.getElementById('customMigrateSource').value.trim();
      const feedback = document.getElementById('customPathFeedback');
      const btnStart = document.getElementById('btnStartCustomMigrate');

      if (!pathInput) {
        showToast('请输入有效的目录路径');
        return;
      }

      feedback.className = 'path-stats-feedback active';
      feedback.innerHTML = '正在分析路径存在性、体积及锁定进程...';
      btnStart.disabled = true;

      try {
        const res = await fetch('/api/check-path', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: pathInput })
        });
        const data = await res.json();

        if (!data.exists) {
          feedback.innerHTML = `<span style="color: var(--status-danger);">指定路径不存在或无权访问</span>`;
          return;
        }

        if (data.is_junction) {
          feedback.innerHTML = `<span style="color: var(--status-junction);">该路径已经是 Junction 软链接，无需重复迁移</span>`;
          return;
        }

        let locksHtml = '';
        if (data.locking_processes && data.locking_processes.length > 0) {
          locksHtml = `
            <div style="margin-top: 6px; color: var(--status-warn);">
              检测到占用进程: ${data.locking_processes.join(', ')}。
              <button class="btn btn-danger" style="padding: 2px 6px; font-size: 11px; margin-left: 6px;" onclick="killLockProcesses(['${data.locking_processes.join("','")}'])">自动关闭进程</button>
            </div>
          `;
        }

        feedback.innerHTML = `
          <div><strong>目录状态良好:</strong> 包含 ${data.file_count} 个文件，占用空间 <strong>${formatBytes(data.size_bytes)}</strong></div>
          ${locksHtml}
        `;
        btnStart.disabled = false;
      } catch (e) {
        feedback.innerHTML = `<span style="color: var(--status-danger);">检查异常: ${e.message}</span>`;
      }
    }

    async function killLockProcesses(procNames) {
      for (const name of procNames) {
        await fetch('/api/kill-process', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: name })
        });
      }
      showToast('已关闭锁定进程，请重新分析');
      analyzeCustomPath();
    }

    // Start Custom Path Migration
    function startCustomPathMigration() {
      const src = document.getElementById('customMigrateSource').value.trim();
      const targetDrive = document.getElementById('customMigrateTargetDrive').value;
      startMigrationProcess(src, targetDrive);
    }

    function triggerPresetMigration(src) {
      startMigrationProcess(src, 'D:');
    }

    async function startMigrationProcess(src, targetDrive) {
      openMigrationModal('正在初始化迁移任务...');

      try {
        const res = await fetch('/api/migrate-start', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ source_path: src, target_drive: targetDrive })
        });
        const data = await res.json();
        if (data.success) {
          pollMigrationStatus();
        } else {
          updateMigrationModalError(data.error || '无法启动任务');
        }
      } catch (e) {
        updateMigrationModalError(e.message);
      }
    }

    function openMigrationModal(title) {
      document.getElementById('migrationModalTitle').innerText = title;
      document.getElementById('migrationProgressBar').style.width = '0%';
      document.getElementById('migrationProgressPercent').innerText = '0%';
      document.getElementById('migrationTransferredBytes').innerText = '0 MB / 0 MB';
      document.getElementById('migrationCurrentFileName').innerText = '正在启动...';
      document.getElementById('migrationModal').classList.add('active');
    }

    function closeMigrationModal() {
      if (state.migrationPollTimer) clearInterval(state.migrationPollTimer);
      document.getElementById('migrationModal').classList.remove('active');
    }

    function updateMigrationModalError(err) {
      if (state.migrationPollTimer) clearInterval(state.migrationPollTimer);
      document.getElementById('migrationModalTitle').innerText = '迁移遇到错误';
      document.getElementById('migrationModalStatusText').innerHTML = `<span style="color: var(--status-danger);">${escapeHtml(err)}</span>`;
    }

    function pollMigrationStatus() {
      if (state.migrationPollTimer) clearInterval(state.migrationPollTimer);

      state.migrationPollTimer = setInterval(async () => {
        try {
          const res = await fetch('/api/migrate-status');
          const data = await res.json();

          if (data.status === 'Running' || data.status === 'Copying') {
            const pct = data.progress_percent || 0;
            document.getElementById('migrationProgressBar').style.width = `${pct}%`;
            document.getElementById('migrationProgressPercent').innerText = `${pct.toFixed(1)}%`;
            document.getElementById('migrationTransferredBytes').innerText = `${formatBytes(data.bytes_copied)} / ${formatBytes(data.total_bytes)}`;
            document.getElementById('migrationCurrentFileName').innerText = data.current_file || '正在传输...';
          } else if (data.status === 'Completed') {
            clearInterval(state.migrationPollTimer);
            document.getElementById('migrationProgressBar').style.width = '100%';
            document.getElementById('migrationProgressPercent').innerText = '100%';
            document.getElementById('migrationModalTitle').innerText = '搬家完成！';
            document.getElementById('migrationModalStatusText').innerText = '数据已全部安全转移，且 NTFS Junction 软链接已在原 C 盘无缝建立。';
            showToast('目录搬家迁移成功完成！');
            loadActiveJunctions();
            runScan();
            refreshDisks();
          } else if (data.status === 'Failed') {
            clearInterval(state.migrationPollTimer);
            updateMigrationModalError(data.error || '迁移失败');
          }
        } catch (e) {
          // ignore transient poll drops
        }
      }, 350);
    }

    // ========================================================================
    // Giant Files Radar
    // ========================================================================
    async function loadGiantFiles() {
      showToast('正在雷达扫描 C 盘 100MB+ 大文件...');
      document.getElementById('giantFilesCounter').innerText = '扫描中...';
      try {
        const res = await fetch('/api/giant-files');
        if (!res.ok) throw new Error('扫描大文件失败');
        state.giantFiles = await res.json();
        document.getElementById('badgeGiantFiles').innerText = state.giantFiles.length;
        document.getElementById('giantFilesCounter').innerText = `已发现 ${state.giantFiles.length} 个超大文件`;
        renderGiantTable();
        showToast(`大文件雷达发现 ${state.giantFiles.length} 个大型资产`);
      } catch (e) {
        showToast('读取大文件失败: ' + e.message);
      }
    }

    function renderGiantTable() {
      const tbody = document.getElementById('giantTableBody');
      tbody.innerHTML = '';

      if (!state.giantFiles || state.giantFiles.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" style="text-align: center; padding: 30px; color: var(--text-tertiary);">
              未发现大于 100MB 的文件
            </td>
          </tr>
        `;
        return;
      }

      const filtered = state.giantFiles.filter(f => {
        if (state.giantFilterCategory !== 'all' && f.category !== state.giantFilterCategory) return false;
        if (state.giantSearchTerm) {
          const q = state.giantSearchTerm.toLowerCase();
          return f.name.toLowerCase().includes(q) || f.path.toLowerCase().includes(q);
        }
        return true;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" style="text-align: center; padding: 30px; color: var(--text-tertiary);">
              未找到符合过滤条件的大文件
            </td>
          </tr>
        `;
        return;
      }

      filtered.forEach(f => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="td-name">${escapeHtml(f.name)}</td>
          <td><span class="badge-pill badge-safe">${escapeHtml(f.category || f.extension)}</span></td>
          <td><span class="path-text" title="${escapeHtml(f.path)}">${escapeHtml(f.path)}</span></td>
          <td style="text-align: right; font-family: var(--font-mono); font-weight: 600; color: #ffffff;">${formatBytes(f.size_bytes)}</td>
          <td style="text-align: center;">
            <div class="table-actions" style="justify-content: center;">
              <button class="icon-action-btn" title="定位文件" onclick="revealInExplorer('${escapeHtml(f.path)}')">
                <svg class="icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/></svg>
              </button>
              <button class="icon-action-btn" title="安全删除文件" onclick="deleteGiantFile('${escapeHtml(f.path)}')">
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
      document.querySelectorAll('#pane-giant .filter-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      renderGiantTable();
    }

    function filterGiantTable() {
      state.giantSearchTerm = document.getElementById('giantSearchInput').value;
      renderGiantTable();
    }

    function deleteGiantFile(path) {
      openConfirmModal(
        '删除大文件确认',
        `确定要永久删除此大文件吗？<br><br><span class="path-text" style="color:#ffffff;">${escapeHtml(path)}</span>`,
        async () => {
          closeConfirmModal();
          showToast('正在删除...');
          try {
            const res = await fetch('/api/delete-file', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ path: path })
            });
            const data = await res.json();
            if (data.success) {
              showToast(`文件已删除，释放 ${formatBytes(data.bytes_freed)}`);
              loadGiantFiles();
              refreshDisks();
            } else {
              showToast('删除失败: ' + (data.errors ? data.errors.join('; ') : '未知原因'));
            }
          } catch (e) {
            showToast('请求失败: ' + e.message);
          }
        }
      );
    }

    // ========================================================================
    // Custom Rules Studio
    // ========================================================================
    async function submitCustomRule() {
      const name = document.getElementById('customRuleName').value.trim();
      const pattern = document.getElementById('customRulePattern').value.trim();

      if (!name || !pattern) {
        showToast('请填写完整的规则名称与路径模式');
        return;
      }

      try {
        const res = await fetch('/api/rules/custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: name, path_pattern: pattern })
        });
        const data = await res.json();
        if (data.success) {
          showToast('规则已成功保存并载入引擎！');
          document.getElementById('customRuleName').value = '';
          document.getElementById('customRulePattern').value = '';
          runScan();
        } else {
          showToast('保存失败: ' + data.error);
        }
      } catch (e) {
        showToast('保存请求异常: ' + e.message);
      }
    }

    // ========================================================================
    // General Confirm Modal
    // ========================================================================
    let onConfirmCallback = null;

    function openConfirmModal(title, bodyHtml, callback) {
      document.getElementById('confirmModalTitle').innerText = title;
      document.getElementById('confirmModalBody').innerHTML = bodyHtml;
      onConfirmCallback = callback;
      document.getElementById('confirmModalBtnAction').onclick = () => {
        if (onConfirmCallback) onConfirmCallback();
      };
      document.getElementById('confirmModal').classList.add('active');
    }

    function closeConfirmModal() {
      document.getElementById('confirmModal').classList.remove('active');
      onConfirmCallback = null;
    }

    // Window Controls
    function minimizeWindow() {
      showToast('快捷键: Win+Down 可最小化本窗口');
    }

    function maximizeWindow() {
      showToast('快捷键: Win+Up 可最大化本窗口');
    }

    async function shutdownApp() {
      openConfirmModal('退出软件', '确定要退出 CleanFlow Pro 智能空间管家吗？', async () => {
        try {
          await fetch('/api/shutdown', { method: 'POST' });
        } catch (e) {}
        window.close();
      });
    }

    // Initialization on DOM Load
    window.addEventListener('DOMContentLoaded', () => {
      refreshDisks();
      runScan();
      loadActiveJunctions();
    });
  </script>
</body>
</html>
'''

if __name__ == '__main__':
    import os
    target_path = os.path.join(os.path.dirname(__file__), 'src', 'ui.html')
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f"Generated Fluent 2 Desktop UI with Browser and Registry: {target_path} ({len(HTML_CONTENT)} bytes)")
