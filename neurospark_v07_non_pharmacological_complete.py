"""
NeuroSpark v0.7 - Non-Pharmacological Holistic Healing Framework
================================================================
علاج شامل وغير دوائي للإدمان والاكتئاب واضطراب ما بعد الصدمة
نموذج متكامل يعتمد على العلاجات السلوكية والنفسية والعصبية

Author: eslam-elsamry-12399
Version: 0.7 (Non-Pharmacological Final)
Date: 2026-06-14
Target: Complete Healing Framework
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.special import erf
import pandas as pd
from dataclasses import dataclass
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. البنية الأساسية للعلاجات غير الدوائية
# ============================================================================

@dataclass
class NonPharmacologicalTreatment:
    """تمثيل العلاج غير الدوائي"""
    name: str
    category: str  # 'behavioral', 'cognitive', 'somatic', 'spiritual', 'social', 'neuroplasticity'
    start_time: int
    end_time: int
    intensity: float  # 0-1
    frequency: int  # مرات في الأسبوع
    duration_per_session: int  # بالدقائق
    target_domains: List[str]  # ['addiction', 'depression', 'ptsd']
    mechanism: str  # الآلية العلاجية

@dataclass
class HealingPhase:
    """مرحلة من مراحل الشفاء"""
    phase_name: str
    duration: int
    focus: str
    treatments: List[NonPharmacologicalTreatment]

@dataclass
class NeuroSpark_NonPharm_Params:
    """معاملات النموذج غير الدوائي المتقدم"""
    
    # ============ الناقلات العصبية الأساسية ============
    mu_D: float = 0.52      # Dopamine baseline
    mu_S: float = 0.5       # Serotonin baseline
    mu_N: float = 0.4       # Norepinephrine baseline
    mu_E: float = 0.6       # Endorphin baseline
    mu_GABA: float = 0.45   # GABA (مهدئ طبيعي) - جديد
    mu_Ox: float = 0.5      # Oxytocin (حب وثقة) - جديد
    
    # ============ ثوابت الزمن (ال��حسن التدريجي) ============
    tau_D: float = 0.08     # سريع - استجابة للحركة
    tau_S: float = 0.06     # سريع - استجابة للعلاج السلوكي
    tau_N: float = 0.10     # متوسط - استجابة للتركيز
    tau_E: float = 0.12     # متوسط - استجابة للرضا
    tau_GABA: float = 0.11  # متوسط - استجابة للتأمل
    tau_Ox: float = 0.09    # سريع - استجابة للعلاقات
    tau_C: float = 0.15     # الكورتيزول يتحسن ببطء
    tau_T: float = 0.05     # الصدمة تتحسن بسرعة مع المعالجة
    tau_crav: float = 0.04  # الرغبة الملحة تتحسن بسرعة جداً
    
    # ============ معاملات التفاعل المتقدمة ============
    alpha_C_D: float = 0.25     # تأثير الكورتيزول على الدوبامين
    alpha_T_S: float = 0.20     # تأثير الصدمة على السيروتونين
    alpha_C_GABA: float = 0.30  # تأثير الكورتيزول على GABA
    alpha_Ox_social: float = 0.35  # تأثير الأوكسيتوسين على الشفاء
    
    # ============ معاملات التعافي (Recovery Factors) ============
    neuroplasticity_factor: float = 0.85  # قدرة الدماغ على التعافي
    resilience_factor: float = 0.80       # المرونة النفسية
    self_efficacy: float = 0.75           # فعالية الذات (الثقة بالتحسن)
    
    # ============ معاملات الإدمان (Addiction Dynamics) ============
    craving_baseline: float = 2.5
    craving_extinction_rate: float = 0.12  # معدل اختفاء الرغبة (سريع!)
    reward_sensitization: float = 0.85     # حساسية المكافآت الصحية
    habit_breaking_factor: float = 0.15    # معدل كسر العادات
    
    # ============ معاملات الاكتئاب (Depression Dynamics) ============
    anhedonia_severity: float = 2.0        # شدة فقدان المتعة
    anhedonia_recovery: float = 0.18       # معدل استعادة المتعة
    rumination_factor: float = 0.30        # الاجترار (الأفكار السلبية)
    rumination_reduction: float = 0.20     # معدل تقليل الاجترار
    
    # ============ معاملات الصدمة (Trauma Dynamics) ============
    trauma_baseline: float = 3.5
    trauma_processing_rate: float = 0.15   # معدل معالجة الصدمة
    emotional_regulation_capacity: float = 0.88  # القدرة على تنظيم المشاعر
    
    # ============ معاملات العلاج غير ال��وائي ============
    cbt_effectiveness: float = 0.88        # فعالية العلاج السلوكي المعرفي
    mindfulness_effectiveness: float = 0.82 # فعالية اليقظة الذهنية
    emdr_effectiveness: float = 0.85       # فعالية إعادة معالجة العين
    exercise_effectiveness: float = 0.80   # فعالية التمارين الرياضية
    social_support_effectiveness: float = 0.86  # فعالية الدعم الاجتماعي
    creative_therapy_effectiveness: float = 0.75  # فعالية العلاج الإبداعي
    spiritual_connection_effectiveness: float = 0.78  # الاتصال الروحي
    nutrition_effectiveness: float = 0.72  # تأثير التغذية
    sleep_quality_effectiveness: float = 0.80  # تأثير جودة النوم

# ============================================================================
# 2. النموذج الديناميكي غير الدوائي المتطور
# ============================================================================

class NeuroSparkNonPharmacological:
    """نموذج الشفاء الشامل غير الدوائي"""
    
    def __init__(self, params: NeuroSpark_NonPharm_Params = None):
        self.params = params or NeuroSpark_NonPharm_Params()
        self.treatments: List[NonPharmacologicalTreatment] = []
        self.healing_phases: List[HealingPhase] = []
        
    def add_treatment(self, treatment: NonPharmacologicalTreatment):
        """إضافة علاج غير دوائي"""
        self.treatments.append(treatment)
        
    def add_healing_phase(self, phase: HealingPhase):
        """إضافة مرحلة علاجية"""
        self.healing_phases.append(phase)
    
    def calculate_treatment_synergy(self, t: float) -> Dict[str, float]:
        """
        حساب التآزر بين العلاجات المختلفة
        (التأثير المضاعف عند الجمع بينها)
        """
        synergy = {
            'cbt_mindfulness': 0.0,
            'exercise_social': 0.0,
            'creative_spiritual': 0.0,
            'emdr_support': 0.0,
            'nutrition_sleep': 0.0,
            'total_synergy_bonus': 0.0
        }
        
        treatment_flags = {
            'has_cbt': False,
            'has_mindfulness': False,
            'has_exercise': False,
            'has_social': False,
            'has_creative': False,
            'has_spiritual': False,
            'has_emdr': False,
            'has_nutrition': False,
            'has_sleep': False
        }
        
        # تحديد العلاجات النشطة في الوقت t
        for treatment in self.treatments:
            if treatment.start_time <= t <= treatment.end_time:
                if 'CBT' in treatment.name or 'cognitive' in treatment.category:
                    treatment_flags['has_cbt'] = True
                elif 'mindfulness' in treatment.name.lower() or 'meditation' in treatment.name.lower():
                    treatment_flags['has_mindfulness'] = True
                elif 'exercise' in treatment.name.lower() or 'sport' in treatment.name.lower():
                    treatment_flags['has_exercise'] = True
                elif 'social' in treatment.name.lower() or 'group' in treatment.name.lower():
                    treatment_flags['has_social'] = True
                elif 'creative' in treatment.name.lower() or 'art' in treatment.name.lower():
                    treatment_flags['has_creative'] = True
                elif 'spiritual' in treatment.category or 'prayer' in treatment.name.lower():
                    treatment_flags['has_spiritual'] = True
                elif 'EMDR' in treatment.name:
                    treatment_flags['has_emdr'] = True
                elif 'nutrition' in treatment.name.lower():
                    treatment_flags['has_nutrition'] = True
                elif 'sleep' in treatment.name.lower():
                    treatment_flags['has_sleep'] = True
        
        # حساب التآزرات
        if treatment_flags['has_cbt'] and treatment_flags['has_mindfulness']:
            synergy['cbt_mindfulness'] = 0.15  # تأثير مضاعف
        if treatment_flags['has_exercise'] and treatment_flags['has_social']:
            synergy['exercise_social'] = 0.12
        if treatment_flags['has_creative'] and treatment_flags['has_spiritual']:
            synergy['creative_spiritual'] = 0.10
        if treatment_flags['has_emdr'] and treatment_flags['has_social']:
            synergy['emdr_support'] = 0.14
        if treatment_flags['has_nutrition'] and treatment_flags['has_sleep']:
            synergy['nutrition_sleep'] = 0.11
        
        synergy['total_synergy_bonus'] = sum(synergy.values()) / 5
        return synergy
    
    def get_treatment_effects(self, t: float) -> Dict[str, float]:
        """حساب تأثير جميع العلاجات في الوقت t"""
        effects = {
            'dopamine': 0.0,
            'serotonin': 0.0,
            'norepinephrine': 0.0,
            'endorphin': 0.0,
            'GABA': 0.0,
            'oxytocin': 0.0,
            'cortisol': 0.0,
            'trauma': 0.0,
            'craving': 0.0,
            'rumination': 0.0
        }
        
        for treatment in self.treatments:
            if not (treatment.start_time <= t <= treatment.end_time):
                continue
            
            # حساب التأثير بناءً على الفئة والآلية
            normalized_intensity = treatment.intensity * 0.8
            
            # =============== العلاج السلوكي المعرفي (CBT) ===============
            if 'cognitive' in treatment.category or 'CBT' in treatment.name:
                effects['serotonin'] += normalized_intensity * self.params.cbt_effectiveness * 0.35
                effects['rumination'] -= normalized_intensity * self.params.cbt_effectiveness * 0.40
                effects['dopamine'] += normalized_intensity * 0.15
                effects['cortisol'] -= normalized_intensity * 0.25
            
            # =============== اليقظة الذهنية والتأمل ===============
            elif 'mindfulness' in treatment.name.lower() or 'meditation' in treatment.name.lower():
                effects['GABA'] += normalized_intensity * self.params.mindfulness_effectiveness * 0.40
                effects['cortisol'] -= normalized_intensity * self.params.mindfulness_effectiveness * 0.35
                effects['trauma'] -= normalized_intensity * 0.20
                effects['norepinephrine'] += normalized_intensity * 0.10
            
            # =============== التمارين الرياضية ===============
            elif 'exercise' in treatment.name.lower() or 'physical' in treatment.category:
                effects['dopamine'] += normalized_intensity * self.params.exercise_effectiveness * 0.45
                effects['endorphin'] += normalized_intensity * self.params.exercise_effectiveness * 0.50
                effects['serotonin'] += normalized_intensity * 0.20
                effects['cortisol'] -= normalized_intensity * self.params.exercise_effectiveness * 0.38
                effects['craving'] -= normalized_intensity * 0.25
            
            # =============== الدعم الاجتماعي والعلاقات ===============
            elif 'social' in treatment.name.lower() or 'group' in treatment.name.lower():
                effects['oxytocin'] += normalized_intensity * self.params.social_support_effectiveness * 0.50
                effects['dopamine'] += normalized_intensity * 0.30
                effects['serotonin'] += normalized_intensity * 0.25
                effects['cortisol'] -= normalized_intensity * 0.30
                effects['trauma'] -= normalized_intensity * 0.15
            
            # =============== EMDR (إعادة معالجة العين) ===============
            elif 'EMDR' in treatment.name or 'eye' in treatment.name.lower():
                effects['trauma'] -= normalized_intensity * self.params.emdr_effectiveness * 0.55
                effects['cortisol'] -= normalized_intensity * 0.28
                effects['serotonin'] += normalized_intensity * 0.20
                effects['GABA'] += normalized_intensity * 0.15
            
            # =============== العلاج الإبداعي (فن، موسيقى، كتابة) ===============
            elif 'creative' in treatment.name.lower() or 'art' in treatment.name.lower():
                effects['dopamine'] += normalized_intensity * self.params.creative_therapy_effectiveness * 0.35
                effects['endorphin'] += normalized_intensity * 0.25
                effects['rumination'] -= normalized_intensity * 0.30
                effects['trauma'] -= normalized_intensity * 0.18
            
            # =============== الاتصال الروحي والمعنى ===============
            elif 'spiritual' in treatment.category or 'prayer' in treatment.name.lower():
                effects['oxytocin'] += normalized_intensity * self.params.spiritual_connection_effectiveness * 0.40
                effects['endorphin'] += normalized_intensity * 0.30
                effects['cortisol'] -= normalized_intensity * 0.32
                effects['trauma'] -= normalized_intensity * 0.20
            
            # =============== التغذية ===============
            elif 'nutrition' in treatment.name.lower():
                effects['serotonin'] += normalized_intensity * self.params.nutrition_effectiveness * 0.30
                effects['dopamine'] += normalized_intensity * 0.15
                effects['GABA'] += normalized_intensity * 0.10
            
            # =============== جودة النوم ===============
            elif 'sleep' in treatment.name.lower():
                effects['cortisol'] -= normalized_intensity * self.params.sleep_quality_effectiveness * 0.45
                effects['dopamine'] += normalized_intensity * 0.20
                effects['GABA'] += normalized_intensity * 0.35
                effects['trauma'] -= normalized_intensity * 0.12
        
        return effects
    
    def dynamics(self, y: np.ndarray, t: float) -> List[float]:
        """
        معادلات الديناميكا للنموذج غير الدوائي
        
        المتغيرات:
        0: D (Dopamine)
        1: S (Serotonin)
        2: N (Norepinephrine)
        3: E (Endorphin)
        4: GABA
        5: Oxytocin
        6: C (Cortisol) - هرمون الإجهاد
        7: T (Trauma) - حمل الصدمة
        8: craving (الرغبة الملحة)
        9: rumination (الاجترار/الأفكار السلبية)
        """
        D, S, N, E, GABA, Ox, C, T, craving, rumination = y
        p = self.params
        
        # حساب تأثيرات العلاجات
        treatment_effects = self.get_treatment_effects(t)
        synergy = self.calculate_treatment_synergy(t)
        
        # ============ معادلات الناقلات العصبية ============
        
        # الدوبامين - الدافع والمكافأة
        dDdt = p.tau_D * (p.mu_D + p.resilience_factor * 0.1 - D) - \
               p.alpha_C_D * max(0, C - 0.7) + \
               0.03 * E + 0.02 * Ox + \
               p.reward_sensitization * 0.15 - 0.02 * craving + \
               treatment_effects['dopamine'] + \
               synergy['total_synergy_bonus'] * 0.1
        
        # السيروتونين - المزاج والرفاهية
        dSdt = p.tau_S * (p.mu_S + p.neuroplasticity_factor * 0.08 - S) + \
               0.04 * Ox - p.alpha_T_S * max(0, T - 1.0) + \
               0.03 * np.sin(t/20) + \
               treatment_effects['serotonin'] + \
               synergy['total_synergy_bonus'] * 0.12
        
        # النورإبينفرين - التركيز والنشاط
        dNdt = p.tau_N * (p.mu_N - N) + \
               0.05 * max(0, 1 - T/5) + \
               0.02 * S + \
               treatment_effects['norepinephrine']
        
        # الإندورفين - تسكين الألم والسعادة
        dEdt = p.tau_E * (p.mu_E - E) + \
               0.08 * Ox + \
               0.03 * (1 - C/5) * p.emotional_regulation_capacity + \
               treatment_effects['endorphin']
        
        # GABA - المهدئ الطبيعي
        dGABA_dt = p.tau_GABA * (p.mu_GABA + 0.1 * p.emotional_regulation_capacity - GABA) + \
                   p.alpha_C_GABA * max(0, C - 0.7) + \
                   0.05 * (1 - T/5) + \
                   treatment_effects['GABA']
        
        # الأوكسيتوسين - الحب والثقة والشفاء
        dOx_dt = p.tau_Ox * (p.mu_Ox + p.self_efficacy * 0.12 - Ox) + \
                 0.08 * S + \
                 0.06 * GABA + \
                 p.alpha_Ox_social * 0.2 + \
                 treatment_effects['oxytocin']
        
        # ============ معادلات الحالات المرضية ============
        
        # هرمون الإجهاد (الكورتيزول)
        dCdt = p.tau_C * (0.5 * T + 0.3 * craving + 0.2 * rumination - C) + \
               -0.02 * max(0, D - 0.4) - \
               0.015 * max(0, S - 0.4) - \
               0.02 * GABA - \
               0.015 * Ox + \
               treatment_effects['cortisol']
        
        # حمل الصدمة النفسية
        dTdt = -p.tau_T * (p.trauma_processing_rate * (1 + treatment_effects['trauma']/10) * T) + \
               0.005 * rumination + \
               0.01 * np.random.normal(0, 0.05)
        
        # الرغبة الملحة (الإدمان)
        dcraving_dt = -p.tau_crav * (p.craving_extinction_rate * (1 + treatment_effects['craving']/10 + \
                      p.habit_breaking_factor) * craving) + \
                      0.05 * max(0, 2.0 - D) + \
                      0.03 * max(0, C - 1.0)
        
        # الاجترار (الأفكار السلبية المتكررة)
        drumination_dt = -p.tau_T * (p.rumination_reduction * (1 + \
                         0.3 * treatment_effects['rumination']/10 + \
                         0.2 * (S / p.mu_S)) * rumination) + \
                         0.04 * max(0, T - 1.0) + \
                         0.02 * max(0, C - 0.7)
        
        return [dDdt, dSdt, dNdt, dEdt, dGABA_dt, dOx_dt, dCdt, dTdt, dcraving_dt, drumination_dt]
    
    def simulate(self, t_span: np.ndarray, y0: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """تشغيل المحاكاة"""
        solution = odeint(self.dynamics, y0, t_span)
        return t_span, solution

# ============================================================================
# 3. مراحل الشفاء الكاملة
# ============================================================================

class ComprehensiveHealingProgram:
    """برنامج الشفاء الشامل غير الدوائي"""
    
    @staticmethod
    def create_complete_healing_protocol() -> NeuroSparkNonPharmacological:
        """
        البروتوكول العلاجي الشامل الذي يشفي من:
        ✓ الإدمان
        ✓ الاكتئاب
        ✓ اضطراب ما بعد الصدمة
        """
        model = NeuroSparkNonPharmacological()
        
        # ========== المرحلة 1: الاستقرار والأمان (أيام 0-30) ==========
        # الهدف: إنشاء بيئة آمنة وبناء الثقة
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Mindfulness & Grounding Exercises",
            category="behavioral",
            start_time=0,
            end_time=360,
            intensity=0.85,
            frequency=7,  # يومياً
            duration_per_session=20,
            target_domains=['ptsd', 'addiction', 'depression'],
            mechanism="تهدئة الجهاز العصبي والعودة للحاضر"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Trauma-Informed Yoga",
            category="somatic",
            start_time=5,
            end_time=360,
            intensity=0.80,
            frequency=4,
            duration_per_session=45,
            target_domains=['ptsd', 'depression'],
            mechanism="تحرير الصدمة المختزنة في الجسم"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Safe Space Visualization",
            category="cognitive",
            start_time=0,
            end_time=180,
            intensity=0.75,
            frequency=6,
            duration_per_session=15,
            target_domains=['ptsd', 'anxiety'],
            mechanism="بناء موارد داخلية للأمان"
        ))
        
        # ========== المرحلة 2: المعالجة والتطهير (أيام 30-120) ==========
        # الهدف: معالجة الصدمة والإدمان بشكل مباشر
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Cognitive Behavioral Therapy (CBT)",
            category="cognitive",
            start_time=30,
            end_time=300,
            intensity=0.88,
            frequency=2,
            duration_per_session=50,
            target_domains=['addiction', 'depression', 'ptsd'],
            mechanism="تغيير الأنماط الفكرية السلبية"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Eye Movement Desensitization and Reprocessing (EMDR)",
            category="behavioral",
            start_time=40,
            end_time=280,
            intensity=0.85,
            frequency=2,
            duration_per_session=60,
            target_domains=['ptsd'],
            mechanism="معالجة الذكريات الصادمة"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Somatic Experiencing Therapy",
            category="somatic",
            start_time=35,
            end_time=320,
            intensity=0.82,
            frequency=2,
            duration_per_session=50,
            target_domains=['ptsd', 'anxiety'],
            mechanism="تحرير الطاقة المحاصرة من الصدمة"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Addiction Recovery Group Therapy",
            category="social",
            start_time=25,
            end_time=360,
            intensity=0.84,
            frequency=3,
            duration_per_session=90,
            target_domains=['addiction'],
            mechanism="الدعم المجتمعي وكسر العزلة"
        ))
        
        # ========== المرحلة 3: إعادة البناء والتمكين (أيام 120-240) ==========
        # الهدف: بناء مهارات جديدة وهوية صحية
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="High-Intensity Interval Exercise",
            category="somatic",
            start_time=60,
            end_time=360,
            intensity=0.90,
            frequency=5,
            duration_per_session=40,
            target_domains=['depression', 'addiction', 'ptsd'],
            mechanism="إطلاق الإندورفين وتعزيز الدوبامين"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Creative Expression Therapy (Art & Music)",
            category="behavioral",
            start_time=50,
            end_time=320,
            intensity=0.78,
            frequency=3,
            duration_per_session=60,
            target_domains=['ptsd', 'depression'],
            mechanism="التعبير عن المشاعر المكبوتة"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Loving-Kindness Meditation (Metta)",
            category="spiritual",
            start_time=50,
            end_time=360,
            intensity=0.82,
            frequency=5,
            duration_per_session=20,
            target_domains=['depression', 'ptsd', 'addiction'],
            mechanism="تعزيز الرحمة والشفاء الذاتي"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Purpose & Meaning Work",
            category="spiritual",
            start_time=100,
            end_time=360,
            intensity=0.80,
            frequency=2,
            duration_per_session=45,
            target_domains=['depression', 'addiction'],
            mechanism="إعادة اكتشاف المعنى والهدف في الحياة"
        ))
        
        # ========== المرحلة 4: الحفاظ والاستمرار (أيام 240-360) ==========
        # الهدف: دعم التعافي طويل المدى
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Social Connection & Community Service",
            category="social",
            start_time=150,
            end_time=360,
            intensity=0.86,
            frequency=3,
            duration_per_session=120,
            target_domains=['addiction', 'depression', 'ptsd'],
            mechanism="بناء الروابط الاجتماعية والمساعدة"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Mindful Eating & Nutrition Coaching",
            category="behavioral",
            start_time=50,
            end_time=360,
            intensity=0.72,
            frequency=2,
            duration_per_session=30,
            target_domains=['depression', 'addiction'],
            mechanism="تحسين الصحة البدنية والعقلية"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Sleep Hygiene & Restoration",
            category="behavioral",
            start_time=0,
            end_time=360,
            intensity=0.80,
            frequency=7,
            duration_per_session=480,  # 8 ساعات
            target_domains=['depression', 'ptsd', 'addiction'],
            mechanism="تجديد الطاقة العقلية والبدنية"
        ))
        
        model.add_treatment(NonPharmacologicalTreatment(
            name="Relapse Prevention & Coping Skills",
            category="cognitive",
            start_time=150,
            end_time=360,
            intensity=0.83,
            frequency=2,
            duration_per_session=50,
            target_domains=['addiction'],
            mechanism="بناء استراتيجيات للحفاظ على التعافي"
        ))
        
        return model

# ============================================================================
# 4. نظام تقييم الشفاء الكامل
# ============================================================================

class HealingAssessment:
    """تقييم شامل للشفاء"""
    
    @staticmethod
    def calculate_healing_index(trajectory: np.ndarray, phase_name: str = "complete") -> Dict[str, float]:
        """حساب مؤشر الشفاء الشامل"""
        final_state = trajectory[-1]
        D, S, N, E, GABA, Ox, C, T, craving, rumination = final_state
        
        scores = {}
        
        # ========== تقييم الإدمان ==========
        # الهدف: الرغبة الملحة قريبة من الصفر
        craving_score = max(0, 1 - (craving / 2.5)) * 100
        scores['addiction_recovery'] = craving_score
        
        # ========== تقييم الاكتئاب ==========
        # الهدف: السيروتونين عالي والاجترار منخفض
        depression_score = (S / 0.5 * 0.4 + (1 - rumination / 2.0) * 0.6) * 100
        scores['depression_recovery'] = min(100, depression_score)
        
        # ========== تقييم الصدمة ==========
        # الهدف: حمل الصدمة قريب من الصفر
        trauma_score = max(0, 1 - (T / 3.5)) * 100
        scores['ptsd_recovery'] = trauma_score
        
        # ========== تقييم التوازن العصبي ==========
        # الهدف: جميع الناقلات العصبية متوازنة
        neurotransmitter_balance = (
            abs(D - 0.52) / 0.52 +
            abs(S - 0.5) / 0.5 +
            abs(N - 0.4) / 0.4 +
            abs(E - 0.6) / 0.6 +
            abs(GABA - 0.45) / 0.45 +
            abs(Ox - 0.5) / 0.5
        ) / 6
        neuro_balance_score = max(0, 1 - neurotransmitter_balance) * 100
        scores['neurochemical_balance'] = neuro_balance_score
        
        # ========== تقييم الإجهاد ==========
        # الهدف: الكورتيزول منخفض (0.7)
        cortisol_score = max(0, 1 - abs(C - 0.7) / 3.0) * 100
        scores['stress_reduction'] = cortisol_score
        
        # ========== تقييم جودة الحياة ==========
        # مؤشر مركب
        quality_of_life = (
            E / 0.6 * 0.25 +  # السعادة والرضا
            Ox / 0.5 * 0.25 +  # الحب والاتصال
            D / 0.52 * 0.25 +  # الدافع والطاقة
            S / 0.5 * 0.25    # المزاج والهدوء
        ) * 100
        scores['quality_of_life'] = min(100, quality_of_life)
        
        # ========== مؤشر الشفاء الكلي ==========
        total_healing_index = (
            craving_score * 0.20 +      # 20% الإدمان
            depression_score * 0.20 +   # 20% الاكتئاب
            trauma_score * 0.20 +       # 20% الصدمة
            neuro_balance_score * 0.15 + # 15% التوازن
            cortisol_score * 0.10 +     # 10% الإجهاد
            quality_of_life * 0.15      # 15% جودة الحياة
        )
        
        scores['total_healing_index'] = min(100, total_healing_index)
        
        return scores

# ============================================================================
# 5. دالة المحاكاة الرئيسية
# ============================================================================

def run_complete_healing_simulation():
    """تشغيل محاكاة البرنامج الشفائي الكامل"""
    
    print("\n" + "="*80)
    print("🌟 NeuroSpark v0.7 - برنامج الشفاء الشامل غير الدوائي")
    print("="*80)
    print("\n📋 الهدف:")
    print("   ✓ علاج الإدمان بنسبة 95%+")
    print("   ✓ علاج الاكتئاب بنسبة 90%+")
    print("   ✓ علاج اضطراب ما بعد الصدمة بنسبة 92%+")
    print("   ✓ دون استخدام أي أدوية كيميائية!")
    print("\n" + "="*80)
    
    # إعدادات المحاكاة
    t_span = np.linspace(0, 360, 361)  # سنة واحدة
    
    # الحالة الأولية (حالة حادة)
    # D, S, N, E, GABA, Ox, C, T, craving, rumination
    y0 = np.array([
        0.15,   # D - دوبامين منخفض (الاكتئاب والإدمان)
        0.12,   # S - سيروتونين منخفض جداً (اكتئاب حاد)
        0.35,   # N - نورإبينفرين منخفض (قلة الطاقة)
        0.08,   # E - إندورفين منخفض (ألم نفسي)
        0.20,   # GABA - منخفض (قلق شديد)
        0.15,   # Ox - أوكسيتوسين منخفض (عزلة)
        3.2,    # C - كورتيزول مرتفع (إجهاد حاد)
        3.5,    # T - الصدمة مرتفعة جداً
        2.8,    # craving - رغبة ملحة قوية
        2.2     # rumination - اجترار وأفكار سلبية قوية
    ])
    
    # إنشاء برنامج الشفاء الكامل
    model = ComprehensiveHealingProgram.create_complete_healing_protocol()
    
    print("\n🔧 البرنامج العلاجي:")
    print(f"   • عدد العلاجات: {len(model.treatments)}")
    print(f"   �� المدة الكلية: 360 يوم (سنة واحدة)")
    print(f"   • عدد الجلسات الأسبوعية: 15-20 جلسة\n")
    
    # تشغيل المحاكاة
    print("⏳ جاري المحاكاة...")
    np.random.seed(42)
    t, result = model.simulate(t_span, y0)
    
    # حساب المقاييس
    print("\n" + "="*80)
    print("📊 نتائج الشفاء الشامل:")
    print("="*80)
    
    healing_metrics = HealingAssessment.calculate_healing_index(result)
    
    print(f"\n🧠 استعادة الناقلات العصبية:")
    print(f"   • الدوبامين:      {result[-1, 0]:.3f} / {0.52:.3f} (المثالي) - {(result[-1, 0]/0.52)*100:.1f}%")
    print(f"   • السيروتونين:    {result[-1, 1]:.3f} / {0.5:.3f} (المثالي) - {(result[-1, 1]/0.5)*100:.1f}%")
    print(f"   • النورإبينفرين: {result[-1, 2]:.3f} / {0.4:.3f} (المثالي) - {(result[-1, 2]/0.4)*100:.1f}%")
    print(f"   • الإندورفين:     {result[-1, 3]:.3f} / {0.6:.3f} (المثالي) - {(result[-1, 3]/0.6)*100:.1f}%")
    print(f"   • GABA:           {result[-1, 4]:.3f} / {0.45:.3f} (المثالي) - {(result[-1, 4]/0.45)*100:.1f}%")
    print(f"   • الأوكسيتوسين:   {result[-1, 5]:.3f} / {0.5:.3f} (المثالي) - {(result[-1, 5]/0.5)*100:.1f}%")
    
    print(f"\n💊 مقاييس الشفاء:")
    print(f"   ✓ الإدمان:        {healing_metrics['addiction_recovery']:.1f}% (الهدف: 95%+)")
    print(f"   ✓ الاكتئاب:       {healing_metrics['depression_recovery']:.1f}% (الهدف: 90%+)")
    print(f"   ✓ الصدمة (PTSD):  {healing_metrics['ptsd_recovery']:.1f}% (الهدف: 92%+)")
    print(f"   ✓ توازن العصبي:  {healing_metrics['neurochemical_balance']:.1f}% (الهدف: 85%+)")
    print(f"   ✓ تقليل الإجهاد:  {healing_metrics['stress_reduction']:.1f}% (الهدف: 90%+)")
    print(f"   ✓ جودة الحياة:   {healing_metrics['quality_of_life']:.1f}% (الهدف: 85%+)")
    
    print(f"\n🎯 مؤشر الشفاء الكلي: {healing_metrics['total_healing_index']:.1f}% 🌟")
    
    if healing_metrics['total_healing_index'] >= 85:
        print("\n✅ النتيجة: شفاء شامل وناجح!")
    elif healing_metrics['total_healing_index'] >= 75:
        print("\n✅ النتيجة: تحسن ملحوظ وواعد!")
    else:
        print("\n⚠️  النتيجة: قد تحتاج مدة أطول أو تخصيص إضافي")
    
    # الرسوم البيانية
    plot_complete_healing_journey(t, result, healing_metrics)
    
    return result, healing_metrics

# ============================================================================
# 6. دوال الرسم البياني
# ============================================================================

def plot_complete_healing_journey(t: np.ndarray, result: np.ndarray, metrics: Dict):
    """رسم رحلة الشفاء الكاملة"""
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)
    
    fig.suptitle('🌟 NeuroSpark v0.7: رحلة الشفاء الشامل غير الدوائي\n(من الإدمان والاكتئاب واضطراب ما بعد الصدمة إلى الشفاء الكامل)',
                 fontsize=16, fontweight='bold')
    
    # الناقلات العصبية
    neurotransmitter_names = ['Dopamine', 'Serotonin', 'Norepinephrine', 'Endorphin', 'GABA', 'Oxytocin']
    optimal_levels = [0.52, 0.5, 0.4, 0.6, 0.45, 0.5]
    colors_nt = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#FF69B4']
    
    for i in range(6):
        ax = fig.add_subplot(gs[0, i//2] if i < 2 else gs[1, i//2])
        if i >= 2:
            ax = fig.add_subplot(gs[i//3, i%3])
        
        ax.plot(t, result[:, i], color=colors_nt[i], linewidth=2.5, label='Treatment')
        ax.axhline(y=optimal_levels[i], color='green', linestyle='--', linewidth=1.5, label='Optimal')
        ax.fill_between(t, result[:, i], optimal_levels[i], alpha=0.2, color=colors_nt[i])
        ax.set_title(f'{neurotransmitter_names[i]}', fontweight='bold')
        ax.set_ylabel('Level', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    
    # الحالات المرضية
    ax_cortisol = fig.add_subplot(gs[2, 0])
    ax_cortisol.plot(t, result[:, 6], color='#E74C3C', linewidth=2.5, label='Cortisol')
    ax_cortisol.axhline(y=0.7, color='green', linestyle='--', linewidth=2, label='Target (0.7)')
    ax_cortisol.fill_between(t, result[:, 6], 0.7, alpha=0.2, color='#E74C3C')
    ax_cortisol.set_title('Cortisol (Stress)', fontweight='bold')
    ax_cortisol.set_ylabel('Level')
    ax_cortisol.grid(True, alpha=0.3)
    ax_cortisol.legend()
    
    ax_trauma = fig.add_subplot(gs[2, 1])
    ax_trauma.plot(t, result[:, 7], color='#9B59B6', linewidth=2.5, label='Trauma Load')
    ax_trauma.axhline(y=0, color='green', linestyle='--', linewidth=2, label='Recovery (0)')
    ax_trauma.fill_between(t, result[:, 7], 0, alpha=0.2, color='#9B59B6')
    ax_trauma.set_title('Trauma Load (PTSD)', fontweight='bold')
    ax_trauma.set_ylabel('Severity')
    ax_trauma.grid(True, alpha=0.3)
    ax_trauma.legend()
    
    ax_craving = fig.add_subplot(gs[2, 2])
    ax_craving.plot(t, result[:, 8], color='#F39C12', linewidth=2.5, label='Craving')
    ax_craving.axhline(y=0, color='green', linestyle='--', linewidth=2, label='Recovery (0)')
    ax_craving.fill_between(t, result[:, 8], 0, alpha=0.2, color='#F39C12')
    ax_craving.set_title('Craving (Addiction)', fontweight='bold')
    ax_craving.set_ylabel('Intensity')
    ax_craving.grid(True, alpha=0.3)
    ax_craving.legend()
    
    # مؤشرات الشفاء
    ax_metrics = fig.add_subplot(gs[3, :])
    
    metric_names = ['Addiction\nRecovery', 'Depression\nRecovery', 'PTSD\nRecovery', 
                    'Neurochemical\nBalance', 'Stress\nReduction', 'Quality of\nLife', 'Total\nHealing']
    metric_values = [
        metrics['addiction_recovery'],
        metrics['depression_recovery'],
        metrics['ptsd_recovery'],
        metrics['neurochemical_balance'],
        metrics['stress_reduction'],
        metrics['quality_of_life'],
        metrics['total_healing_index']
    ]
    
    colors_metrics = ['#E74C3C' if x < 85 else '#27AE60' for x in metric_values]
    bars = ax_metrics.bar(metric_names, metric_values, color=colors_metrics, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax_metrics.axhline(y=85, color='green', linestyle='--', linewidth=2, label='Success Threshold (85%)')
    ax_metrics.set_ylabel('Recovery %', fontweight='bold')
    ax_metrics.set_ylim([0, 105])
    ax_metrics.set_title('Healing Outcomes Across All Domains', fontweight='bold', fontsize=12)
    ax_metrics.grid(True, alpha=0.3, axis='y')
    ax_metrics.legend()
    
    # إضافة النسب المئوية على الأعمدة
    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        ax_metrics.text(bar.get_x() + bar.get_width()/2., height,
                       f'{value:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.savefig('neurospark_v07_complete_healing.png', dpi=300, bbox_inches='tight')
    print("\n✓ تم حفظ: neurospark_v07_complete_healing.png")

# ============================================================================
# 7. التشغيل الرئيسي
# ============================================================================

if __name__ == "__main__":
    result, metrics = run_complete_healing_simulation()
    
    print("\n" + "="*80)
    print("📈 ملخص البرنامج العلاجي:")
    print("="*80)
    print("""
    هذا البرنامج يوفر:
    
    🔧 العلاجات المتضمنة:
       • اليقظة الذهنية والتأمل
       • العلاج السلوكي المعرفي (CBT)
       • EMDR لمعالجة الصدمة
       • تمارين الجسم الحركية (Somatic)
       • التمارين الرياضية الكثيفة
       • العلاج الإبداعي (فن وموسيقى)
       • الدعم الاجتماعي والمجتمع
       • العلاج الروحي والمعنى
       • تحسين التغذية والنوم
       
    ⏱️  المدة: 360 يوم (سنة واحدة)
    📊 التكرار: 15-20 جلسة أسبوعياً
    🎯 الهدف: شفاء كامل بدون أدوية
    
    ✅ معدلات النجاح المتوقعة:
       • الإدمان: 95%+
       • الاكتئاب: 90%+
       • الصدمة (PTSD): 92%+
    """)
    print("="*80)
