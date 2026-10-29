import streamlit as st

# 페이지 기본 설정 (웹 브라우저 탭 타이틀 및 레이아웃)
st.set_page_config(
    page_title="열역학 기반 스마트 냉난방 절전 도우미",
    page_icon="🌡️",
    layout="wide"
)

def calculate_heat_loss(temp_in, temp_out, area, insulation_level):
    """
    기계공학 열역학 공식(Q = U * A * dT)을 이용한 열손실량 연산
    """
    u_values = {
        "1등급 (우수: 3중창 / 최신 단열재)": 0.3,
        "2등급 (보통: 이중창 / 일반 벽체)": 0.6,
        "3등급 (미흡: 단창 / 노후 건물)": 1.2
    }
    u_val = u_values.get(insulation_level, 0.6)
    delta_t = abs(temp_in - temp_out)
    heat_loss = u_val * area * delta_t
    return heat_loss, u_val

# 메인 타이틀 및 소개
st.title("🌡️ [기계공학 융합] 열역학 기반 스마트 냉난방 절전 도우미")
st.markdown("열전달 공식($Q = U \\cdot A \\cdot \\Delta T$)을 적용하여 실내 열손실량을 연산하고, 계절별 최적 에너지 제어 가이드를 제공합니다.")

st.divider()

# 사용자 입력 구역 (2개 열로 구분)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 환경 정보 입력")
    temp_in = st.number_input("현재 실내 온도 (°C)", value=22.0, step=0.5, format="%.1f")
    temp_out = st.number_input("현재 실외 온도 (°C)", value=2.0, step=0.5, format="%.1f")
    humidity_in = st.number_input("현재 실내 습도 (%)", value=35.0, min_value=0.0, max_value=100.0, step=1.0)

with col2:
    st.subheader("2. 공간 및 단열 정보 입력")
    room_area = st.number_input("벽면 및 창문 총 면적 (m²)", value=20.0, min_value=1.0, step=1.0)
    insulation = st.selectbox(
        "건물 단열 등급 선택",
        [
            "1등급 (우수: 3중창 / 최신 단열재)",
            "2등급 (보통: 이중창 / 일반 벽체)",
            "3등급 (미흡: 단창 / 노후 건물)"
        ],
        index=1
    )

st.divider()

# 열역학 연산 실행
heat_loss, u_val = calculate_heat_loss(temp_in, temp_out, room_area, insulation)
delta_t = abs(temp_in - temp_out)
is_winter = temp_out < temp_in

# 연산 결과 시각화
st.header("📊 열역학 분석 및 에너지 리포트")

m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("실내외 온도차 (ΔT)", f"{delta_t:.1f} °C")
m_col2.metric("열관류율 (U값)", f"{u_val} W/m²K")
m_col3.metric("추정 열손실(취득)량", f"{heat_loss:.2f} W")

st.write("")

# 최적 제어 및 가이드 피드백
if is_winter:
    target_temp = 20.0
    st.info("❄️ **계절 구분:** 겨울철 난방 모드")
    if temp_in > 22.0:
        saving = (temp_in - target_temp) * 7
        st.warning(f"⚠️ 현재 설정 온도가 높습니다. 희망 온도를 {target_temp}°C로 낮추면 난방비를 약 **{saving:.1f}%** 절약할 수 있습니다.")
    else:
        st.success("✅ 적정 난방 온도를 유지하고 있습니다.")

    if humidity_in < 40:
        st.caption("💧 **가습 제안:** 습도가 낮아 체감 온도가 떨어집니다. 가습기를 가동하여 습도를 50%로 유지를 권장합니다.")
else:
    target_temp = 26.0
    st.info("☀️ **계절 구분:** 여름철 냉방 모드")
    if temp_in < 24.0:
        saving = (target_temp - temp_in) * 6
        st.warning(f"⚠️ 현재 설정 온도가 낮습니다. 희망 온도를 {target_temp}°C로 올려 설정하면 전기세를 약 **{saving:.1f}%** 절약할 수 있습니다.")
    else:
        st.success("✅ 적정 냉방 온도를 유지하고 있습니다.")

# 단열 개선 팁
st.divider()
st.subheader("🔧 기계공학적 단열 개선 팁")
if "3등급" in insulation:
    st.error("• 현재 건물 단열이 미흡합니다. 문풍지/뽁뽁이 설치 시 열관류율(U값)이 감소하여 열손실을 최대 30% 줄일 수 있습니다.")
else:
    st.success("• 단열 상태가 양호합니다. 환기 시스템 제어로 실내 공기질을 관리해 주세요.")
