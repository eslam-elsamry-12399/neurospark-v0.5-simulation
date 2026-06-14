"""
NeuroSpark v0.6 - Advanced Therapeutic Model with Multi-Scenario Simulation
===========================================================================
تحسينات رئيسية:
1. معاملات علاجية جديدة (Pharmacological + Behavioral Interventions)
2. نموذج ديناميكي محسّن مع تأثيرات غير خطية
3. اختبار سيناريوهات متعددة (6 سيناريوهات مختلفة)
4. تقييم فعالية العلاج (Efficacy Metrics)
5. تحليل حساسية المعاملات (Sensitivity Analysis)

Author: eslam-elsamry-12399
Version: 0.6
Date: 2026-06-14
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
import pandas as pd
import seaborn as sns
from dataclasses import dataclass
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. تعريف هياكل البيانات المتقدمة
# ============================================================================

@dataclass
class TherapeuticIntervention:
    """تمثيل التدخل العلاجي"""
    name: str
    start_time: int
    end_time: int
    intensity: float  # 0-1
    target: str      # 'dopamine', 'cortisol', 'trauma', 'all'
    mechanism: str   # 'agonist', 'antagonist', 'modulation', 'behavioral'
    
@dataclass
class PatientProfile:
    """ملف المريض العلاجي"""
    patient_id: str
    severity_level: str  # 'mild', 'moderate', 'severe'
    comorbidity_type: str  # 'ptsd', 'addiction', 'both'
    treatment_history: str  # 'naive', 'resistant', 'responsive'

@dataclass
class NeuroSpark_Params:
    """معاملات النموذج المتقدمة"""
    # معاملات أساسية
    mu_D: float = 0.52      # Dopamine baseline
    mu_S: float = 0.5       # Serotonin baseline
    mu_N: float = 0.4       # Norepinephrine baseline
    mu_E: float = 0.6       # Endorphin baseline
    
    # معاملات الديناميكا
    tau_D: float = 0.1      # Dopamine time constant
    tau_S: float = 0.08     # Serotonin time constant
    tau_N: float = 0.12     # Norepinephrine time constant
    tau_E: float = 0.15     # Endorphin time constant
    tau_C: float = 0.2      # Cortisol time constant
    tau_T: float = 0.08     # Trauma time constant
    
    # معاملات التفاعل (مشاركة عصبية)
    alpha: float = 0.3      # Dopamine-Cortisol coupling
    beta: float = 0.1       # Stress feedback
    gamma: float = 0.15     # Trauma effect on neurotransmitters
    delta: float = 0.05     # Self-reinforcing craving
    
    # معاملات الصدمة والإدمان
    craving_amplitude: float = 0.5
    craving_decay: float = 0.1
    trauma_sensitivity: float = 1.5
    
    # معاملات العلاج (جديدة)
    medication_efficacy: float = 0.8
    behavioral_efficacy: float = 0.6
    psychotherapy_efficacy: float = 0.5

# ============================================================================
# 2. النموذج الديناميكي المحسّن
# ============================================================================

class NeuroSparkV06:
    """نموذج NeuroSpark v0.6 المتطور"""
    
    def __init__(self, params: NeuroSpark_Params = None):
        self.params = params or NeuroSpark_Params()
        self.interventions: List[TherapeuticIntervention] = []
        
    def add_intervention(self, intervention: TherapeuticIntervention):
        """إضافة تدخل علاجي"""
        self.interventions.append(intervention)
        
    def get_intervention_effect(self, t: float) -> Dict[str, float]:
        """حساب تأثير التدخلات العلاجية في الوقت t"""
        effects = {
            'dopamine': 0.0,
            'serotonin': 0.0,
            'norepinephrine': 0.0,
            'endorphin': 0.0,
            'cortisol': 0.0,
            'trauma': 0.0
        }
        
        for intervention in self.interventions:
            if intervention.start_time <= t <= intervention.end_time:
                progress = (t - intervention.start_time) / max(1, intervention.end_time - intervention.start_time)
                effect_magnitude = intervention.intensity * np.exp(-0.05 * progress)
                
                if intervention.target == 'all':
                    targets = ['dopamine', 'serotonin', 'norepinephrine', 'endorphin']
                else:
                    targets = [intervention.target]
                
                for target in targets:
                    if intervention.mechanism == 'agonist':
                        effects[target] += effect_magnitude * 0.3
                    elif intervention.mechanism == 'antagonist':
                        effects[target] -= effect_magnitude * 0.2
                    elif intervention.mechanism == 'modulation':
                        effects[target] += effect_magnitude * 0.15
                    
                if intervention.target == 'cortisol' or intervention.target == 'all':
                    effects['cortisol'] -= effect_magnitude * 0.25
                    
                if intervention.target == 'trauma' or intervention.target == 'all':
                    effects['trauma'] -= effect_magnitude * 0.2
        
        return effects
    
    def dynamics(self, y: np.ndarray, t: float) -> List[float]:
        """معادلات الديناميكا المتقدمة"""
        D, S, N, E, C, Trauma = y
        p = self.params
        
        # تأثيرات التدخل العلاجي
        interventions = self.get_intervention_effect(t)
        
        # نموذج الرغبة الملحة (Hawkes Process)
        craving = p.craving_amplitude * np.exp(-p.craving_decay * t) * \
                  (1 + 0.3 * np.sin(t/10)) * (1 + p.delta * max(0, C - 1.0))
        
        # معادلات الديناميكا الأساسية مع التحسينات
        dDdt = p.tau_D * (p.mu_D - D) - p.alpha * max(0, C - 1.0) + \
               0.02 * E - 0.01 * craving + \
               0.05 * Trauma * np.exp(-t/50) + \
               interventions['dopamine']
        
        dSdt = p.tau_S * (p.mu_S - S) + 0.03 * np.cos(t/10) + \
               interventions['serotonin']
        
        dNdt = p.tau_N * (p.mu_N - N) + p.gamma * Trauma * np.exp(-t/50) + \
               0.1 * np.sin(t/15) + \
               interventions['norepinephrine']
        
        dEdt = p.tau_E * (p.mu_E - E) - 0.04 * max(0, C - 1.0) + \
               0.02 * S + \
               interventions['endorphin']
        
        # معادلة الكورتيزول (الحاجز الحرج)
        dCdt = p.tau_C * (p.trauma_sensitivity * Trauma - C) + \
               0.05 * craving + \
               0.02 * np.random.normal(0, 0.01) + \
               interventions['cortisol']
        
        # معادلة حمل الصدمة
        dTraumadt = -0.08 * Trauma + 0.01 * np.random.normal(0, 0.05) + \
                    interventions['trauma']
        
        # تأثيرات غير خطية (nonlinear feedback)
        if C > 2.0:  # Extreme stress response
            dDdt *= 0.7
            dSdt *= 0.6
            dEdt *= 0.5
        
        return [dDdt, dSdt, dNdt, dEdt, dCdt, dTraumadt]
    
    def simulate(self, t_span: np.ndarray, y0: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """تشغيل المحاكاة"""
        solution = odeint(self.dynamics, y0, t_span)
        return t_span, solution

# ============================================================================
# 3. السيناريوهات العلاجية المختلفة
# ============================================================================

class TherapyScenarios:
    """تعريف السيناريوهات العلاجية المختلفة"""
    
    @staticmethod
    def create_scenario_1_baseline() -> NeuroSparkV06:
        """السيناريو 1: خط أساسي (بدون علاج)"""
        model = NeuroSparkV06()
        return model
    
    @staticmethod
    def create_scenario_2_ssri_only() -> NeuroSparkV06:
        """السيناريو 2: علاج SSRI فقط (مثبطات امتصاص السيروتونين الانتقائية)"""
        model = NeuroSparkV06()
        model.add_intervention(TherapeuticIntervention(
            name="SSRI (Sertraline)",
            start_time=50,
            end_time=400,
            intensity=0.85,
            target='serotonin',
            mechanism='agonist'
        ))
        return model
    
    @staticmethod
    def create_scenario_3_combination_pharmacological() -> NeuroSparkV06:
        """السيناريو 3: علاج دوائي متوازن (SSRI + بوبروبيون)"""
        model = NeuroSparkV06()
        model.add_intervention(TherapeuticIntervention(
            name="SSRI (Sertraline)",
            start_time=50,
            end_time=400,
            intensity=0.8,
            target='serotonin',
            mechanism='agonist'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Bupropion (DA/NE reuptake inhibitor)",
            start_time=75,
            end_time=400,
            intensity=0.75,
            target='dopamine',
            mechanism='agonist'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Cortisol Modulation",
            start_time=100,
            end_time=400,
            intensity=0.7,
            target='cortisol',
            mechanism='modulation'
        ))
        return model
    
    @staticmethod
    def create_scenario_4_psychotherapy() -> NeuroSparkV06:
        """السيناريو 4: العلاج السلوكي المعرفي (CBT + Mindfulness)"""
        model = NeuroSparkV06()
        model.add_intervention(TherapeuticIntervention(
            name="Cognitive Behavioral Therapy",
            start_time=30,
            end_time=400,
            intensity=0.65,
            target='trauma',
            mechanism='modulation'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Mindfulness-Based Stress Reduction",
            start_time=40,
            end_time=400,
            intensity=0.55,
            target='cortisol',
            mechanism='modulation'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Endorphin Enhancement (Exercise)",
            start_time=20,
            end_time=400,
            intensity=0.5,
            target='endorphin',
            mechanism='agonist'
        ))
        return model
    
    @staticmethod
    def create_scenario_5_integrated_treatment() -> NeuroSparkV06:
        """السيناريو 5: العلاج المتكامل (دوائي + سلوكي نفسي)"""
        model = NeuroSparkV06()
        # المرحلة 1: تثبيت
        model.add_intervention(TherapeuticIntervention(
            name="Initial SSRI",
            start_time=30,
            end_time=200,
            intensity=0.9,
            target='serotonin',
            mechanism='agonist'
        ))
        # المرحلة 2: توسيع + علاج نفسي
        model.add_intervention(TherapeuticIntervention(
            name="Dopamine Agonist",
            start_time=60,
            end_time=350,
            intensity=0.8,
            target='dopamine',
            mechanism='agonist'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Trauma-Focused Therapy",
            start_time=100,
            end_time=400,
            intensity=0.75,
            target='trauma',
            mechanism='modulation'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Cortisol Regulation",
            start_time=120,
            end_time=400,
            intensity=0.7,
            target='cortisol',
            mechanism='modulation'
        ))
        return model
    
    @staticmethod
    def create_scenario_6_advanced_personalized() -> NeuroSparkV06:
        """السيناريو 6: العلاج الشخصي المتقدم (AI-guided)"""
        model = NeuroSparkV06()
        params = model.params
        params.medication_efficacy = 0.95
        params.behavioral_efficacy = 0.75
        params.psychotherapy_efficacy = 0.7
        
        # علاج متدرج وديناميكي
        model.add_intervention(TherapeuticIntervention(
            name="Adaptive SSRI + Antipsychotic",
            start_time=20,
            end_time=380,
            intensity=0.92,
            target='serotonin',
            mechanism='agonist'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Real-time Cortisol Feedback",
            start_time=50,
            end_time=400,
            intensity=0.88,
            target='cortisol',
            mechanism='modulation'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="VR-based Exposure Therapy",
            start_time=80,
            end_time=350,
            intensity=0.8,
            target='trauma',
            mechanism='modulation'
        ))
        model.add_intervention(TherapeuticIntervention(
            name="Neurofeedback + Meditation",
            start_time=100,
            end_time=400,
            intensity=0.78,
            target='all',
            mechanism='modulation'
        ))
        return model

# ============================================================================
# 4. نظام تقييم الفعالية
# ============================================================================

class EfficacyAssessment:
    """تقييم فعالية العلاج"""
    
    @staticmethod
    def calculate_remission_rate(trajectory: np.ndarray) -> float:
        """نسبة الهدوء (Remission Rate)"""
        final_state = trajectory[-1]
        D, S, N, E, C, Trauma = final_state
        
        optimal_D = 0.52
        optimal_S = 0.5
        optimal_C = 0.7  # هدف الكورتيزول
        
        error = (abs(D - optimal_D) + abs(S - optimal_S) + abs(C - optimal_C)) / 3
        remission = max(0, 1 - error)
        return remission
    
    @staticmethod
    def calculate_symptom_reduction(baseline: np.ndarray, treated: np.ndarray) -> Dict[str, float]:
        """تقليل الأعراض في كل متغير"""
        metrics = {}
        labels = ['Dopamine', 'Serotonin', 'Norepinephrine', 'Endorphin', 'Cortisol', 'Trauma']
        
        for i, label in enumerate(labels):
            baseline_final = baseline[-1, i]
            treated_final = treated[-1, i]
            
            if i == 4:  # Cortisol - نريد تقليله
                reduction = max(0, (baseline_final - treated_final) / max(baseline_final, 0.01))
            elif i == 5:  # Trauma - نريد تقليله
                reduction = max(0, (baseline_final - treated_final) / max(baseline_final, 0.01))
            else:
                reduction = 1 - abs(treated_final - baseline_final) / max(abs(baseline_final), 0.01)
            
            metrics[label.lower()] = min(1.0, max(0, reduction))
        
        return metrics
    
    @staticmethod
    def calculate_time_to_stability(trajectory: np.ndarray, stability_window: int = 50) -> int:
        """الوقت المطلوب للوصول إلى الاستقرار"""
        C = trajectory[:, 4]  # Cortisol
        target = 0.7
        threshold = 0.15
        
        for i in range(len(C) - stability_window):
            window = C[i:i+stability_window]
            if np.all(np.abs(window - target) < threshold):
                return i
        
        return len(C)

# ============================================================================
# 5. دالة المحاكاة الرئيسية
# ============================================================================

def run_comprehensive_simulation():
    """تشغيل المحاكاة الشاملة"""
    
    # إعدادات المحاكاة
    t_span = np.linspace(0, 400, 401)
    y0 = np.array([0.1, 0.1, 0.8, 0.05, 4.0, 3.0])  # حالة مرضية أولية
    
    # إنشاء السيناريوهات
    scenarios = {
        'Baseline (No Treatment)': TherapyScenarios.create_scenario_1_baseline(),
        'SSRI Only': TherapyScenarios.create_scenario_2_ssri_only(),
        'Pharmacological Combo': TherapyScenarios.create_scenario_3_combination_pharmacological(),
        'Psychotherapy': TherapyScenarios.create_scenario_4_psychotherapy(),
        'Integrated Treatment': TherapyScenarios.create_scenario_5_integrated_treatment(),
        'Advanced Personalized': TherapyScenarios.create_scenario_6_advanced_personalized(),
    }
    
    # تشغيل المحاكاات
    results = {}
    baseline_result = None
    
    print("🚀 بدء المحاكاة الشاملة...")
    print("=" * 70)
    
    for scenario_name, model in scenarios.items():
        np.random.seed(42)  # للحصول على نتائج متسقة
        t, y = model.simulate(t_span, y0)
        results[scenario_name] = y
        
        if scenario_name == 'Baseline (No Treatment)':
            baseline_result = y
        
        print(f"✓ {scenario_name}: محاكاة مكتملة")
    
    # حساب المقاييس
    print("\n" + "=" * 70)
    print("📊 تقييم الفعالية:")
    print("=" * 70)
    
    metrics_df = []
    
    for scenario_name, trajectory in results.items():
        remission = EfficacyAssessment.calculate_remission_rate(trajectory)
        
        if baseline_result is not None and scenario_name != 'Baseline (No Treatment)':
            symptom_reduction = EfficacyAssessment.calculate_symptom_reduction(baseline_result, trajectory)
            time_to_stability = EfficacyAssessment.calculate_time_to_stability(trajectory)
        else:
            symptom_reduction = {k: 0 for k in ['dopamine', 'serotonin', 'norepinephrine', 'endorphin', 'cortisol', 'trauma']}
            time_to_stability = 400
        
        cortisol_final = trajectory[-1, 4]
        trauma_final = trajectory[-1, 5]
        
        metrics_df.append({
            'Scenario': scenario_name,
            'Remission Rate': remission,
            'Cortisol Final': cortisol_final,
            'Trauma Final': trauma_final,
            'Time to Stability': time_to_stability,
            'Cortisol Reduction %': symptom_reduction['cortisol'] * 100,
            'Trauma Reduction %': symptom_reduction['trauma'] * 100,
        })
        
        print(f"\n{scenario_name}:")
        print(f"  • نسبة الهدوء: {remission*100:.1f}%")
        print(f"  • الكورتيزول النهائي: {cortisol_final:.2f} (الهدف: 0.7)")
        print(f"  • حمل الصدمة النهائي: {trauma_final:.2f}")
        print(f"  • الوقت للاستقرار: {time_to_stability} وحدة زمنية")
        print(f"  • تقليل الكورتيزول: {symptom_reduction['cortisol']*100:.1f}%")
        print(f"  • تقليل الصدمة: {symptom_reduction['trauma']*100:.1f}%")
    
    metrics_dataframe = pd.DataFrame(metrics_df)
    
    # الرسوم البيانية
    plot_comprehensive_results(t_span, results)
    plot_efficacy_comparison(metrics_dataframe)
    plot_sensitivity_analysis(scenarios, t_span, y0)
    
    return results, metrics_dataframe

# ============================================================================
# 6. دوال الرسم البياني
# ============================================================================

def plot_comprehensive_results(t_span: np.ndarray, results: Dict[str, np.ndarray]):
    """رسم النتائج الشاملة"""
    fig, axs = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle('NeuroSpark v0.6: مقارنة السيناريوهات العلاجية المختلفة', fontsize=16, fontweight='bold')
    
    labels = ['Dopamine (DA)', 'Serotonin (5-HT)', 'Norepinephrine (NE)', 
              'Endorphin (β-EP)', 'Cortisol', 'Trauma Load']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    axs = axs.ravel()
    
    for i in range(6):
        for scenario_name, trajectory in results.items():
            linestyle = '-' if scenario_name == 'Baseline (No Treatment)' else '--'
            linewidth = 2.5 if scenario_name == 'Baseline (No Treatment)' else 1.5
            alpha = 0.7 if scenario_name == 'Baseline (No Treatment)' else 0.6
            
            axs[i].plot(t_span, trajectory[:, i], label=scenario_name, 
                       linestyle=linestyle, linewidth=linewidth, alpha=alpha)
        
        axs[i].set_title(labels[i], fontsize=12, fontweight='bold')
        axs[i].set_xlabel('الوقت (وحدة زمنية)', fontsize=10)
        axs[i].set_ylabel('التركيز (mmol/L)', fontsize=10)
        axs[i].grid(True, alpha=0.3)
        axs[i].legend(fontsize=8, loc='best')
        
        # إضافة خطوط الهدف
        if i == 4:  # Cortisol
            axs[i].axhline(y=0.7, color='green', linestyle=':', linewidth=2, label='Target Cortisol', alpha=0.7)
        elif i == 5:  # Trauma
            axs[i].axhline(y=0, color='green', linestyle=':', linewidth=2, label='Target Trauma', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('neurospark_v06_comprehensive_scenarios.png', dpi=300, bbox_inches='tight')
    print("\n✓ تم حفظ: neurospark_v06_comprehensive_scenarios.png")

def plot_efficacy_comparison(metrics_df: pd.DataFrame):
    """مقارنة الفعالية"""
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('NeuroSpark v0.6: مقاييس فعالية العلاج', fontsize=16, fontweight='bold')
    
    # الرسم 1: نسبة الهدوء
    axs[0, 0].barh(metrics_df['Scenario'], metrics_df['Remission Rate'] * 100, color='#FF6B6B')
    axs[0, 0].set_xlabel('نسبة الهدوء (%)', fontsize=11)
    axs[0, 0].set_title('معدل الهدوء والاستجابة', fontsize=12, fontweight='bold')
    axs[0, 0].grid(True, alpha=0.3)
    
    # الرسم 2: الكورتيزول النهائي
    colors_cortisol = ['red' if x > 1.0 else 'orange' if x > 0.7 else 'green' 
                       for x in metrics_df['Cortisol Final']]
    axs[0, 1].barh(metrics_df['Scenario'], metrics_df['Cortisol Final'], color=colors_cortisol)
    axs[0, 1].axvline(x=0.7, color='green', linestyle='--', linewidth=2, label='Target')
    axs[0, 1].set_xlabel('مستوى الكورتيزول النهائي', fontsize=11)
    axs[0, 1].set_title('التحكم في الكورتيزول', fontsize=12, fontweight='bold')
    axs[0, 1].legend()
    axs[0, 1].grid(True, alpha=0.3)
    
    # الرسم 3: تقليل الكورتيزول
    axs[1, 0].barh(metrics_df['Scenario'], metrics_df['Cortisol Reduction %'], color='#4ECDC4')
    axs[1, 0].set_xlabel('نسبة التقليل (%)', fontsize=11)
    axs[1, 0].set_title('تقليل الكورتيزول مقارنة بالخط الأساسي', fontsize=12, fontweight='bold')
    axs[1, 0].grid(True, alpha=0.3)
    
    # الرسم 4: تقليل الصدمة
    axs[1, 1].barh(metrics_df['Scenario'], metrics_df['Trauma Reduction %'], color='#45B7D1')
    axs[1, 1].set_xlabel('نسبة التقليل (%)', fontsize=11)
    axs[1, 1].set_title('تقليل حمل الصدمة', fontsize=12, fontweight='bold')
    axs[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('neurospark_v06_efficacy_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ تم حفظ: neurospark_v06_efficacy_metrics.png")

def plot_sensitivity_analysis(scenarios: Dict, t_span: np.ndarray, y0: np.ndarray):
    """تحليل الحساسية للمعاملات"""
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('NeuroSpark v0.6: تحليل حساسية المعاملات', fontsize=16, fontweight='bold')
    
    base_model = scenarios['Integrated Treatment']
    base_t, base_result = base_model.simulate(t_span, y0)
    
    # اختبار حساسية: معدل الدواء
    sensitivities = {'medication_efficacy': [0.5, 0.75, 0.9, 1.0],
                    'behavioral_efficacy': [0.3, 0.5, 0.7, 0.9],
                    'trauma_sensitivity': [1.0, 1.25, 1.5, 2.0],
                    'craving_decay': [0.05, 0.1, 0.15, 0.2]}
    
    for idx, (param_name, values) in enumerate(sensitivities.items()):
        ax = axs[idx // 2, idx % 2]
        
        for val in values:
            model = scenarios['Integrated Treatment']
            model.params.__dict__[param_name] = val
            t, result = model.simulate(t_span, y0)
            cortisol_trajectory = result[:, 4]
            ax.plot(t, cortisol_trajectory, label=f'{param_name}={val}', linewidth=1.5)
        
        ax.set_xlabel('الوقت (وحدة زمنية)', fontsize=10)
        ax.set_ylabel('مستوى الكورتيزول', fontsize=10)
        ax.set_title(f'حساسية: {param_name}', fontsize=11, fontweight='bold')
        ax.axhline(y=0.7, color='green', linestyle='--', alpha=0.5, label='Target')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    
    plt.tight_layout()
    plt.savefig('neurospark_v06_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ تم حفظ: neurospark_v06_sensitivity_analysis.png")

# ============================================================================
# 7. التشغيل الرئيسي
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧠 NeuroSpark v0.6 - نموذج العلاج العصبي المتطور")
    print("="*70)
    print("\nتطوير: eslam-elsamry-12399")
    print("التاريخ: 2026-06-14")
    print("="*70)
    
    results, metrics_df = run_comprehensive_simulation()
    
    # طباعة النتائج إلى ملف CSV
    metrics_df.to_csv('neurospark_v06_metrics.csv', index=False)
    print("\n✓ تم حفظ: neurospark_v06_metrics.csv")
    
    print("\n" + "="*70)
    print("✨ اكتملت المحاكاة بنجاح!")
    print("="*70)
    print("\nالملفات المُنتجة:")
    print("  1. neurospark_v06_comprehensive_scenarios.png")
    print("  2. neurospark_v06_efficacy_metrics.png")
    print("  3. neurospark_v06_sensitivity_analysis.png")
    print("  4. neurospark_v06_metrics.csv")
    print("\n" + "="*70)
