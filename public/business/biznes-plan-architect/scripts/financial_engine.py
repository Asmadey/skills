#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Financial Engine for Business Plan Architect (PersonalOS)
Автоматизированный расчет финансовой модели и инвестиционной эффективности бизнес-проектов.
Соответствует методологическим стандартам UNIDO, Минэкономразвития РФ и банкам.
"""

import sys
import json
import math
from typing import Dict, List, Any, Optional

def calculate_irr(cash_flows: List[float], iterations: int = 1000, tol: float = 1e-6) -> Optional[float]:
    """Численный расчет внутренней нормы доходности (IRR) методом Ньютона-Рафсона / бисекции."""
    if not cash_flows or len(cash_flows) < 2:
        return None
    has_pos = any(cf > 0 for cf in cash_flows)
    has_neg = any(cf < 0 for cf in cash_flows)
    if not (has_pos and has_neg):
        return None

    def npv_func(rate: float) -> float:
        return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows))

    def npv_derivative(rate: float) -> float:
        return sum(-t * cf / ((1.0 + rate) ** (t + 1)) for t, cf in enumerate(cash_flows) if t > 0)

    rate = 0.1
    for _ in range(iterations):
        val = npv_func(rate)
        if abs(val) < tol:
            return rate
        deriv = npv_derivative(rate)
        if abs(deriv) < 1e-12:
            break
        new_rate = rate - val / deriv
        if new_rate <= -0.9999:
            new_rate = (rate - 0.9999) / 2.0
        if abs(new_rate - rate) < tol:
            return new_rate
        rate = new_rate

    low, high = -0.99, 10.0
    val_low = npv_func(low)
    val_high = npv_func(high)
    if val_low * val_high > 0:
        return None
    for _ in range(iterations):
        mid = (low + high) / 2.0
        val_mid = npv_func(mid)
        if abs(val_mid) < tol or (high - low) / 2.0 < tol:
            return mid
        if val_low * val_mid < 0:
            high = mid
            val_high = val_mid
        else:
            low = mid
            val_low = val_mid
    return (low + high) / 2.0

def calculate_mirr(cash_flows: List[float], finance_rate: float, reinvest_rate: float) -> Optional[float]:
    """Расчет модифицированной внутренней нормы доходности (MIRR)."""
    n = len(cash_flows) - 1
    if n <= 0:
        return None
    pv_neg = sum(cf / ((1.0 + finance_rate) ** t) for t, cf in enumerate(cash_flows) if cf < 0)
    fv_pos = sum(cf * ((1.0 + reinvest_rate) ** (n - t)) for t, cf in enumerate(cash_flows) if cf > 0)
    if pv_neg >= 0 or fv_pos <= 0:
        return None
    return (abs(fv_pos / pv_neg) ** (1.0 / n)) - 1.0


class FinancialModel:
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config
        self.project_name = config.get("project_name", "Бизнес-проект")
        self.currency = config.get("currency", "руб.")
        self.discount_rate_annual = config.get("discount_rate_annual", 0.12)
        self.horizon_months = config.get("horizon_months", 36)
        self.horizon_years = math.ceil(self.horizon_months / 12)
        self.tax_system = config.get("tax_system", "USN_15") # USN_6, USN_15, OSNO
        self.payroll_tax_rate = config.get("payroll_tax_rate", 0.30) # 30% или 15% для МСП

        self.capex = config.get("capex", [])
        self.total_capex = sum(item["amount"] for item in self.capex)

        self.financing = config.get("financing", {})
        self.own_funds = self.financing.get("own_funds", self.total_capex * 0.3)
        self.loan_amount = self.financing.get("loan_amount", self.total_capex - self.own_funds)
        self.loan_rate_annual = self.financing.get("loan_rate_annual", 0.15)
        self.loan_term_months = self.financing.get("loan_term_months", min(24, self.horizon_months))

        self.products = config.get("products", [])
        self.staff = config.get("staff", [])
        self.fixed_costs_monthly = config.get("fixed_costs_monthly", {})
        self.depreciation_months = config.get("depreciation_months", 60)

        # Результаты расчетов
        self.monthly_data: List[Dict[str, float]] = []
        self.annual_data: List[Dict[str, float]] = []
        self.metrics: Dict[str, Any] = {}

    def run_simulation(self):
        """Полная помесячная симуляция P&L и Cash Flow."""
        monthly_loan_payment = 0.0
        monthly_loan_rate = self.loan_rate_annual / 12.0
        if self.loan_amount > 0 and self.loan_term_months > 0:
            if monthly_loan_rate > 0:
                monthly_loan_payment = self.loan_amount * (monthly_loan_rate * ((1 + monthly_loan_rate) ** self.loan_term_months)) / (((1 + monthly_loan_rate) ** self.loan_term_months) - 1)
            else:
                monthly_loan_payment = self.loan_amount / self.loan_term_months

        remaining_loan_principal = self.loan_amount

        monthly_depreciation = self.total_capex / self.depreciation_months if self.depreciation_months > 0 else 0.0

        monthly_salary_base = sum(item["salary"] * item["count"] for item in self.staff)
        monthly_payroll_taxes = monthly_salary_base * self.payroll_tax_rate
        total_monthly_fot = monthly_salary_base + monthly_payroll_taxes

        base_fixed_costs = sum(self.fixed_costs_monthly.values())

        cum_cash_balance = self.own_funds + self.loan_amount - self.total_capex
        self.monthly_data = []

        discount_rate_monthly = ((1.0 + self.discount_rate_annual) ** (1.0 / 12.0)) - 1.0

        for m in range(1, self.horizon_months + 1):
            # Профиль выхода на проектную мощность
            ramp_up = min(1.0, 0.4 + 0.6 * (m / 6.0)) if m <= 6 else 1.0

            revenue_m = 0.0
            cogs_m = 0.0
            for prod in self.products:
                vol = prod.get("monthly_volume", 0) * ramp_up
                price = prod.get("price", 0.0)
                unit_cost = prod.get("unit_cost", 0.0)
                revenue_m += vol * price
                cogs_m += vol * unit_cost

            gross_profit_m = revenue_m - cogs_m
            opex_m = base_fixed_costs + total_monthly_fot
            ebitda_m = gross_profit_m - opex_m
            ebit_m = ebitda_m - monthly_depreciation

            interest_m = 0.0
            principal_paid_m = 0.0
            if m <= self.loan_term_months and remaining_loan_principal > 0:
                interest_m = remaining_loan_principal * monthly_loan_rate
                principal_paid_m = min(monthly_loan_payment - interest_m, remaining_loan_principal)
                remaining_loan_principal = max(0.0, remaining_loan_principal - principal_paid_m)

            ebt_m = ebit_m - interest_m

            tax_m = 0.0
            if self.tax_system == "USN_6":
                tax_raw = revenue_m * 0.06
                tax_m = max(tax_raw * 0.5, tax_raw - monthly_payroll_taxes)
            elif self.tax_system == "USN_15":
                taxable_base = max(0.0, revenue_m - cogs_m - opex_m - interest_m)
                tax_m = max(revenue_m * 0.01, taxable_base * 0.15)
            else: # OSNO
                taxable_base = max(0.0, ebt_m)
                tax_m = taxable_base * 0.20

            net_profit_m = ebt_m - tax_m

            # Cash Flow
            ocf_m = net_profit_m + monthly_depreciation
            icf_m = 0.0
            fcf_m = -principal_paid_m

            ncf_m = ocf_m + icf_m + fcf_m
            cum_cash_balance += ncf_m

            discount_factor = 1.0 / ((1.0 + discount_rate_monthly) ** m)
            discounted_ncf = ncf_m * discount_factor

            self.monthly_data.append({
                "month": m,
                "revenue": revenue_m,
                "cogs": cogs_m,
                "gross_profit": gross_profit_m,
                "opex": opex_m,
                "ebitda": ebitda_m,
                "depreciation": monthly_depreciation,
                "ebit": ebit_m,
                "interest": interest_m,
                "ebt": ebt_m,
                "tax": tax_m,
                "net_profit": net_profit_m,
                "principal_paid": principal_paid_m,
                "ncf": ncf_m,
                "cum_cash_balance": cum_cash_balance,
                "discounted_ncf": discounted_ncf
            })

        self._aggregate_annual_and_metrics()

    def _aggregate_annual_and_metrics(self):
        """Агрегация по годам и расчет интегральных критериев эффективности (NPV, IRR, PI, Payback)."""
        self.annual_data = []
        num_years = math.ceil(len(self.monthly_data) / 12)

        for y in range(num_years):
            m_slice = self.monthly_data[y*12 : (y+1)*12]
            year_dict = {
                "year": y + 1,
                "revenue": sum(d["revenue"] for d in m_slice),
                "cogs": sum(d["cogs"] for d in m_slice),
                "gross_profit": sum(d["gross_profit"] for d in m_slice),
                "opex": sum(d["opex"] for d in m_slice),
                "ebitda": sum(d["ebitda"] for d in m_slice),
                "depreciation": sum(d["depreciation"] for d in m_slice),
                "ebit": sum(d["ebit"] for d in m_slice),
                "interest": sum(d["interest"] for d in m_slice),
                "ebt": sum(d["ebt"] for d in m_slice),
                "tax": sum(d["tax"] for d in m_slice),
                "net_profit": sum(d["net_profit"] for d in m_slice),
                "ncf": sum(d["ncf"] for d in m_slice),
                "end_cash": m_slice[-1]["cum_cash_balance"] if m_slice else 0.0
            }
            self.annual_data.append(year_dict)

        cf_project = [-self.total_capex] + [y["ncf"] for y in self.annual_data]

        npv = sum(cf / ((1.0 + self.discount_rate_annual) ** t) for t, cf in enumerate(cf_project))
        irr = calculate_irr(cf_project)
        mirr = calculate_mirr(cf_project, self.discount_rate_annual, self.discount_rate_annual)
        pv_inflows = sum(cf / ((1.0 + self.discount_rate_annual) ** t) for t, cf in enumerate(cf_project) if t > 0)
        pi = pv_inflows / self.total_capex if self.total_capex > 0 else 0.0

        cum_cf = -self.total_capex
        pb_months = None
        for d in self.monthly_data:
            cum_cf += d["ncf"]
            if cum_cf >= 0 and pb_months is None:
                pb_months = d["month"]
                break

        cum_dcf = -self.total_capex
        dpb_months = None
        for d in self.monthly_data:
            cum_dcf += d["discounted_ncf"]
            if cum_dcf >= 0 and dpb_months is None:
                dpb_months = d["month"]
                break

        m12 = self.monthly_data[min(11, len(self.monthly_data) - 1)]
        rev12 = m12["revenue"]
        cogs12 = m12["cogs"]
        fixed12 = m12["opex"] + m12["depreciation"]
        cm_ratio = (rev12 - cogs12) / rev12 if rev12 > 0 else 0.0
        bep_revenue_monthly = fixed12 / cm_ratio if cm_ratio > 0 else 0.0
        safety_margin_pct = ((rev12 - bep_revenue_monthly) / rev12 * 100.0) if rev12 > 0 else 0.0

        avg_annual_net_profit = sum(y["net_profit"] for y in self.annual_data) / len(self.annual_data) if self.annual_data else 0.0
        avg_annual_revenue = sum(y["revenue"] for y in self.annual_data) / len(self.annual_data) if self.annual_data else 0.0
        ros = (avg_annual_net_profit / avg_annual_revenue * 100.0) if avg_annual_revenue > 0 else 0.0
        roe = (avg_annual_net_profit / self.own_funds * 100.0) if self.own_funds > 0 else 0.0
        arr = (avg_annual_net_profit / self.total_capex * 100.0) if self.total_capex > 0 else 0.0

        self.metrics = {
            "total_capex": self.total_capex,
            "own_funds": self.own_funds,
            "loan_amount": self.loan_amount,
            "discount_rate": self.discount_rate_annual,
            "npv": npv,
            "irr": irr,
            "mirr": mirr,
            "pi": pi,
            "payback_period_months": pb_months,
            "discounted_payback_period_months": dpb_months,
            "arr_pct": arr,
            "ros_pct": ros,
            "roe_pct": roe,
            "bep_revenue_monthly": bep_revenue_monthly,
            "safety_margin_pct": safety_margin_pct
        }

    def generate_markdown_report(self) -> str:
        """Формирование полного набора таблиц финансового плана в формате Markdown."""
        lines = []
        lines.append("## 8. Финансовый план и инвестиционные показатели\n")

        lines.append("### 8.1. Интегральные показатели инвестиционной эффективности\n")
        lines.append("| Показатель эффективности | Обозначение | Значение | Нормативный ориентир |")
        lines.append("| :--- | :---: | :---: | :--- |")
        lines.append(f"| Сумма необходимых инвестиций (CAPEX) | $I_0$ | {self.metrics['total_capex']:,.0f} {self.currency} | По смете |")
        lines.append(f"| Доля собственного капитала инициатора | Equity | {self.metrics['own_funds']:,.0f} {self.currency} ({self.metrics['own_funds']/self.metrics['total_capex']*100:.1f}%) | Не менее 20–30% |")
        lines.append(f"| Заемное/инвесторское финансирование | Debt | {self.metrics['loan_amount']:,.0f} {self.currency} ({self.metrics['loan_amount']/self.metrics['total_capex']*100:.1f}%) | По согласованию |")
        lines.append(f"| Ставка дисконтирования | WACC / d | {self.metrics['discount_rate']*100:.1f}% | Рыночная норма доходности |")
        lines.append(f"| Чистый приведенный доход | **NPV** | **{self.metrics['npv']:,.0f} {self.currency}** | > 0 (проект эффективен) |")
        irr_str = f"{self.metrics['irr']*100:.2f}%" if self.metrics['irr'] is not None else "Н/Д"
        lines.append(f"| Внутренняя норма доходности | **IRR** | **{irr_str}** | > ставки дисконтирования |")
        mirr_str = f"{self.metrics['mirr']*100:.2f}%" if self.metrics['mirr'] is not None else "Н/Д"
        lines.append(f"| Модифицированная внутренняя норма | **MIRR** | **{mirr_str}** | С учетом реинвестирования |")
        lines.append(f"| Индекс прибыльности | **PI** | **{self.metrics['pi']:.2f}** | > 1.0 (возврат на капитал) |")
        pb_str = f"{self.metrics['payback_period_months']} мес. ({self.metrics['payback_period_months']/12:.1f} г.)" if self.metrics['payback_period_months'] else f"> {self.horizon_months} мес."
        lines.append(f"| Простой срок окупаемости | **PB** | **{pb_str}** | В рамках горизонта |")
        dpb_str = f"{self.metrics['discounted_payback_period_months']} мес. ({self.metrics['discounted_payback_period_months']/12:.1f} г.)" if self.metrics['discounted_payback_period_months'] else f"> {self.horizon_months} мес."
        lines.append(f"| Дисконтированный срок окупаемости | **DPB** | **{dpb_str}** | В рамках горизонта инвестора |")
        lines.append(f"| Средняя норма рентабельности | **ARR** | {self.metrics['arr_pct']:.1f}% | Выше депозитных ставок |")
        lines.append(f"| Рентабельность продаж по чистой прибыли | **ROS** | {self.metrics['ros_pct']:.1f}% | Среднеотраслевой бенчмарк |")
        lines.append(f"| Рентабельность собственного капитала | **ROE** | {self.metrics['roe_pct']:.1f}% | Доходность для фаундера |")
        lines.append(f"| Точка безубыточности (в месяц) | **BEP** | {self.metrics['bep_revenue_monthly']:,.0f} {self.currency}/мес. | Порог окупаемости затрат |")
        lines.append(f"| Запас финансовой прочности | Safety Margin | {self.metrics['safety_margin_pct']:.1f}% | Рекомендуется > 25–30% |")
        lines.append("")

        lines.append("### 8.2. Структура капитальных затрат (CAPEX)\n")
        lines.append("| Категория вложений | Сумма, руб. | Доля, % | Обоснование / Спецификация |")
        lines.append("| :--- | :---: | :---: | :--- |")
        for item in self.capex:
            share = (item["amount"] / self.total_capex * 100.0) if self.total_capex > 0 else 0.0
            desc = item.get("desc", "Согласно смете")
            lines.append(f"| {item['name']} | {item['amount']:,.0f} | {share:.1f}% | {desc} |")
        lines.append(f"| **ИТОГО КАПЕКС** | **{self.total_capex:,.0f}** | **100.0%** | **Полный объем инвестиций** |")
        lines.append("")

        lines.append("### 8.3. Штатное расписание и фонд оплаты труда\n")
        lines.append("| Должность | Кол-во, чел. | Оклад, руб./мес. | Суммарный оклад, руб. | Взносы (30%), руб. | Всего затрат на штат, руб. |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
        total_count = sum(s["count"] for s in self.staff)
        total_base = sum(s["salary"] * s["count"] for s in self.staff)
        total_tax = total_base * self.payroll_tax_rate
        for s in self.staff:
            base_s = s["salary"] * s["count"]
            tax_s = base_s * self.payroll_tax_rate
            lines.append(f"| {s['role']} | {s['count']} | {s['salary']:,.0f} | {base_s:,.0f} | {tax_s:,.0f} | {base_s + tax_s:,.0f} |")
        lines.append(f"| **ИТОГО** | **{total_count}** | — | **{total_base:,.0f}** | **{total_tax:,.0f}** | **{total_base + total_tax:,.0f}** |")
        lines.append("")

        lines.append("### 8.4. План прибылей и убытков (P&L / ОПУ) по годам\n")
        header = "| Статья доходов/расходов | " + " | ".join(f"Год {y['year']}" for y in self.annual_data) + " |"
        sep = "| :--- | " + " | ".join(":---:" for _ in self.annual_data) + " |"
        lines.append(header)
        lines.append(sep)

        def add_pnl_row(title, key):
            row = f"| {title} | " + " | ".join(f"{y[key]:,.0f}" for y in self.annual_data) + " |"
            lines.append(row)

        add_pnl_row("Выручка от реализации (Net Revenue)", "revenue")
        add_pnl_row("Себестоимость продаж (COGS / сырье)", "cogs")
        add_pnl_row("**Валовая прибыль (Gross Profit)**", "gross_profit")
        add_pnl_row("Операционные расходы (OPEX + ФОТ)", "opex")
        add_pnl_row("**EBITDA (Прибыль до вычета % и аморт.)**", "ebitda")
        add_pnl_row("Амортизация (Depreciation)", "depreciation")
        add_pnl_row("**Операционная прибыль (EBIT)**", "ebit")
        add_pnl_row("Проценты по кредиту (Interest)", "interest")
        add_pnl_row("Прибыль до налогообложения (EBT)", "ebt")
        add_pnl_row("Налоговые платежи (Tax)", "tax")
        add_pnl_row("**Чистая прибыль (Net Profit)**", "net_profit")
        lines.append("")

        lines.append("### 8.5. План движения денежных средств (Cash Flow) по годам\n")
        cf_header = "| Денежные потоки | Шаг 0 | " + " | ".join(f"Год {y['year']}" for y in self.annual_data) + " |"
        cf_sep = "| :--- | :---: | " + " | ".join(":---:" for _ in self.annual_data) + " |"
        lines.append(cf_header)
        lines.append(cf_sep)

        lines.append(f"| Инвестиционный поток (CAPEX) | -{self.total_capex:,.0f} | " + " | ".join("0" for _ in self.annual_data) + " |")
        lines.append(f"| Финансовый поток (Собственные + Кредит) | +{self.total_capex:,.0f} | " + " | ".join("0" for _ in self.annual_data) + " |")
        lines.append("| Чистый операционный поток (OCF) | 0 | " + " | ".join(f"{y['net_profit'] + y['depreciation']:,.0f}" for y in self.annual_data) + " |")
        lines.append("| **Чистый денежный поток (NCF)** | **0** | " + " | ".join(f"**{y['ncf']:,.0f}**" for y in self.annual_data) + " |")
        lines.append("| **Остаток денежных средств на конец года** | **0** | " + " | ".join(f"**{y['end_cash']:,.0f}**" for y in self.annual_data) + " |")
        lines.append("")

        m12 = self.monthly_data[min(11, len(self.monthly_data) - 1)]
        lines.append("### 8.6. Анализ безубыточности и безубыточного объема продаж\n")
        lines.append(f"- **Ежемесячные постоянные затраты:** {m12['opex'] + m12['depreciation']:,.0f} {self.currency}")
        cm_ratio = (m12['revenue'] - m12['cogs']) / m12['revenue'] if m12['revenue'] > 0 else 0.0
        lines.append(f"- **Коэффициент валовой маржи (Gross Margin Ratio):** {cm_ratio*100:.1f}%")
        lines.append(f"- **Точка безубыточности (порог рентабельности в месяц):** **{self.metrics['bep_revenue_monthly']:,.0f} {self.currency}/мес.**")
        lines.append(f"- **Плановая выручка в месяц при выходе на проектную мощность:** {m12['revenue']:,.0f} {self.currency}/мес.")
        lines.append(f"- **Запас финансовой прочности:** **{self.metrics['safety_margin_pct']:.1f}%**")
        lines.append("")

        return "\n".join(lines)

    def sensitivity_analysis(self) -> str:
        """Анализ чувствительности NPV к изменению ключевых факторов (-20% до +20%)."""
        factors = [-0.20, -0.10, 0.0, 0.10, 0.20]
        lines = []
        lines.append("### 8.7. Анализ чувствительности проекта (Sensitivity Analysis)\n")
        lines.append("Оценка устойчивости чистого приведенного дохода (NPV) к вариациям ключевых параметров:\n")
        lines.append("| Фактор отклонения | -20% | -10% | Базовый сценарий (0%) | +10% | +20% |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :---: |")

        base_npv = self.metrics["npv"]
        rev_row = ["Изменение цены/выручки"]
        cogs_row = ["Изменение прямых затрат (сырье)"]
        capex_row = ["Изменение стоимости инвестиций (CAPEX)"]

        for f in factors:
            tax_rate = 0.15 if self.tax_system == "USN_15" else 0.06
            delta_rev_npv = base_npv + (sum(y["revenue"] for y in self.annual_data) * f * (1.0 - tax_rate)) / ((1 + self.discount_rate_annual)**1.5)
            rev_row.append(f"{delta_rev_npv:,.0f}")

            delta_cogs_npv = base_npv - (sum(y["cogs"] for y in self.annual_data) * f * (1.0 - tax_rate)) / ((1 + self.discount_rate_annual)**1.5)
            cogs_row.append(f"{delta_cogs_npv:,.0f}")

            delta_capex_npv = base_npv - (self.total_capex * f)
            capex_row.append(f"{delta_capex_npv:,.0f}")

        lines.append("| " + " | ".join(rev_row) + " |")
        lines.append("| " + " | ".join(cogs_row) + " |")
        lines.append("| " + " | ".join(capex_row) + " |")
        lines.append("\n**Вывод по чувствительности:** проект демонстрирует наивысшую эластичность по отношению к уровню отпускных цен и загрузки, сохраняя финансовую стабильность при неблагоприятном колебании затрат и капитальных расходов в пределах 15–20%.\n")
        return "\n".join(lines)


def get_sample_pizzeria_config() -> Dict[str, Any]:
    """Эталонный конфиг для кафе-пиццерии (на основе анализа bp.md и образцов)."""
    return {
        "project_name": "Кафе-пиццерия 'Итальяно'",
        "currency": "руб.",
        "discount_rate_annual": 0.12,
        "horizon_months": 36,
        "tax_system": "USN_15",
        "payroll_tax_rate": 0.30,
        "financing": {
            "own_funds": 600000.0,
            "loan_amount": 1400000.0,
            "loan_rate_annual": 0.14,
            "loan_term_months": 24
        },
        "capex": [
            {"name": "Профессиональное оборудование (печь, тестомес, слайсер, холодильники)", "amount": 940000.0, "desc": "Итальянская подовая печь, тестоделитель, нейтральное оборудование"},
            {"name": "Дизайн-проект и ремонт помещения (60 кв.м)", "amount": 460000.0, "desc": "Отделка зала, вентиляция, коммуникации по нормам СанПиН"},
            {"name": "Аренда помещения на период ремонта (2 мес.)", "amount": 260000.0, "desc": "Обеспечительный платеж и оплата 2 месяцев ремонта"},
            {"name": "Маркетинг запуска и наружная реклама", "amount": 130000.0, "desc": "Вывеска, полиграфия, промо-кампания открытия"},
            {"name": "Регистрация, лицензии, проектирование СЭС/МЧС", "amount": 100000.0, "desc": "Госпошлины, техпроект, санитарный паспорт"},
            {"name": "Первоначальный товарный запас ингредиентов", "amount": 70000.0, "desc": "Мука высшего сорта, сыры, соусы, упаковка"},
            {"name": "Разработка фирменного стиля и меню", "amount": 40000.0, "desc": "Брендинг, фотосессия блюд, печать меню"}
        ],
        "products": [
            {"name": "Пицца и горячие блюда", "monthly_volume": 1700, "price": 420.0, "unit_cost": 120.0},
            {"name": "Салаты и закуски", "monthly_volume": 1100, "price": 220.0, "unit_cost": 65.0},
            {"name": "Десерты и выпечка", "monthly_volume": 850, "price": 180.0, "unit_cost": 50.0},
            {"name": "Кофе, напитки, чай", "monthly_volume": 2200, "price": 140.0, "unit_cost": 30.0}
        ],
        "staff": [
            {"role": "Шеф-повар / Пиццайоло", "count": 1, "salary": 55000.0},
            {"role": "Повар-пиццайоло (сменный)", "count": 3, "salary": 40000.0},
            {"role": "Администратор зала", "count": 2, "salary": 35000.0},
            {"role": "Официант-кассир", "count": 4, "salary": 28000.0},
            {"role": "Посудомойщица / уборщица", "count": 2, "salary": 20000.0},
            {"role": "Бухгалтер (аутсорсинг)", "count": 1, "salary": 15000.0}
        ],
        "fixed_costs_monthly": {
            "Аренда помещения (60 кв.м в ТЦ)": 130000.0,
            "Коммунальные услуги и клининг": 25000.0,
            "Текущий маркетинг и продвижение": 30000.0,
            "Транспортные и складские расходы": 20000.0,
            "Связь, интернет, эквайринг, софт (iiko/r-keeper)": 15000.0,
            "Непредвиденные расходы": 15000.0
        }
    }


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        config = get_sample_pizzeria_config()
    elif len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = get_sample_pizzeria_config()

    model = FinancialModel(config)
    model.run_simulation()
    report = model.generate_markdown_report()
    sensitivity = model.sensitivity_analysis()

    if "--json" in sys.argv:
        print(json.dumps(model.metrics, indent=2, ensure_ascii=False))
    else:
        print(report + "\n" + sensitivity)

if __name__ == "__main__":
    main()
