import streamlit as st
from streamlit_image_viewer import image_viewer
import  streamlit_toggle as tog
import polars as pl
from glob import glob 
from pathlib import Path
import os

ROOTDIR = Path(__file__).parent
NUM_PATIENTS = len(glob(os.path.join(ROOTDIR, "data") + "/patient_*"))
PATIENT_IDS = sorted([int(Path(patient_id).name.replace("patient_","")) for patient_id in glob(os.path.join(ROOTDIR, "data") + "/patient_*")])

# page config
st.set_page_config(layout="wide")

# define functions and class
class Patient:
    def __init__(self, patient_id: int, condition: str):
        self.patient_id = patient_id
        self.name = f"patient_{patient_id}"
        self.patient_index = PATIENT_IDS.index(patient_id)
        self.patient_path = os.path.join(ROOTDIR,"data",self.name)
        if condition == "全て表示":
            self.pre_image_path_list = glob(os.path.join(self.patient_path, "Pre")+"/*")
            self.post_image_path_list = glob(os.path.join(self.patient_path, "Post")+"/*")
        else:
            self.pre_image_path_list = glob(os.path.join(self.patient_path, "Pre") + f"/*{condition}*")
            self.post_image_path_list = glob(os.path.join(self.patient_path, "Post") + f"/*{condition}*")
    
def plus_index():
    if st.session_state.patient_index == NUM_PATIENTS - 1:
        st.session_state.patient_index = 0
    else:   
        st.session_state.patient_index += 1
    
def minss_index():
    st.session_state.patient_index -= 1
    
def record_df():
    st.session_state.df = st.session_state.df.with_columns(
        pl.when(pl.col("ID")==st.session_state.patient_id)
        .then(st.session_state.result)
        .otherwise(pl.col("術前治療効果判定"))
        .alias("術前治療効果判定")
        )
    download_df()

def download_df():
    st.session_state.df.write_excel(f"{st.session_state.project_name}.xlsx")

def main():
    # initialize session state
    if "patient_index" not in st.session_state:
        st.session_state.patient_index = 0
    if "state" not in st.session_state:
        st.session_state.state = 0
    if "ncol" not in st.session_state:
        st.session_state.ncol = 3
    if "nrow" not in st.session_state:
        st.session_state.nrow = 2
        
        
    # >>>>> first page <<<<<
    with st.sidebar:
        if st.session_state.state == 0:
            st.markdown("# Response Recorder")
            st.radio('start', ['新規記録', '記録を再開'], label_visibility='hidden', key='radio_start')
            
            if st.session_state.radio_start == "新規記録":
                st.session_state.project_name = st.text_input(label="プロジェクト名")
                st.session_state.df = pl.DataFrame([pl.Series(name="ID",values=PATIENT_IDS), pl.Series(name="術前治療効果判定",values=["未判定" for i in range(NUM_PATIENTS)])])
                
                if st.button("記録開始"):
                    st.session_state.state = 1
                    if st.session_state.project_name == "":
                        st.session_state.state = 0
                        st.warning("プロジェクト名を入力してください")
                    else:
                        st.experimental_rerun()
            
            elif st.session_state.radio_start == "記録を再開":
                file = st.file_uploader(label="記録を再開", accept_multiple_files=False, key="upload_file")
                if file is not None:
                    st.session_state.project_name = file.name.replace(".xlsx","")
                    st.session_state.df = pl.read_excel(file)
                
                if st.button("記録開始"):
                    st.session_state.state = 1
                    if file is None:
                        st.session_state.state = 0
                        st.warning("再開するexcelファイルを選択してください")
                    else:
                        st.experimental_rerun()
            
    # >>>>> Record page <<<<<
    # ===== sidebar =====
    if st.session_state.state == 1:
        
        with st.sidebar:
            st.markdown("# Response Recorder")
            # ----- settings -----
            with st.expander("### :gear: 画像の表示設定"):
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.ncol = st.number_input("**number of columns**", min_value=1, step=1, value=st.session_state.ncol)
                with col2:
                    st.session_state.nrow = st.number_input("**number of rows**", min_value=1, step=1,value=st.session_state.nrow)
                is_visible_image_name = tog.st_toggle_switch(label="画像名の表示", 
                    key="is_visible_image_name", 
                    default_value=True, 
                    label_after = False, 
                    inactive_color = '#D3D3D3', 
                    active_color="#11567f", 
                    track_color="#29B5E8"
                    )

            st.markdown(f"### :large_blue_square: プロジェクト名 : **{st.session_state.project_name}**")
            
            st.markdown("### :large_blue_square: 患者の選択	")
            _,col = st.columns([0.1,0.9])
            with col:
                st.select_slider("", PATIENT_IDS, value=PATIENT_IDS[st.session_state.patient_index], key="patient_id", label_visibility="collapsed")
            
            _, side_col1, side_col2 = st.columns([0.1,0.45,0.45])
            with side_col1:
                st.button("<< 前の患者へ", on_click=minss_index)
            with side_col2:
                st.button("次の患者へ >>", on_click=plus_index)
            
            # ----- condition -----
            st.markdown("### :large_blue_square: 表示する撮影条件")
            _,col = st.columns([0.1,0.9])
            with col:
                condition = st.radio(
                    "",
                    ["全て表示", "normal", "iod", "NBI"],
                    horizontal=True,
                    key="condition",
                    label_visibility="collapsed"
                    )

            st.markdown("### :large_blue_square: 判定の選択")
            with st.form("submit"):
                st.radio(
                    "**術前治療効果判定**",
                    ["PD", "SD", "PR", "CR", "未判定"],
                    horizontal=True,
                    key="result",
                    )
                _,_,_,col = st.columns(4)
                with col:
                    st.form_submit_button("反映", on_click=record_df)
            
            # ----- view and save df -----
            st.markdown("### :large_blue_square: Record結果の表示/出力")
            _,col = st.columns([0.1,0.9])
            with col:
                if st.button("Download Excel file", key="save_file", on_click=download_df):
                    st.info(f"ダウンロードしました {ROOTDIR}/{st.session_state.project_name}.xlsx")
                st.dataframe(st.session_state.df, hide_index=True)
            
        
        
        # ===== content =====
        patient = Patient(patient_id=st.session_state.patient_id, condition=st.session_state.condition)
        style = """
                .highlight-box {
                            display: inline-block;
                            padding: 5px;
                            border-radius: 5px;
                             color: #0078ff;
                            font-family: Arial;
                        }
                """
        st.markdown(
            f"""
            <div>
                <h3>患者ID : <span class="highlight-box">patient_{st.session_state.patient_id}</span></h3>
                <h3>現在の判定 : <span class="highlight-box">{st.session_state.df.filter(pl.col('ID')==st.session_state.patient_id)['術前治療効果判定'].item()}</span></h3>
            </div>
            <style>
                {style}
            </style>

            """, unsafe_allow_html=True)

        pre_col, post_col = st.columns(2)
        with pre_col:
            st.markdown("## Pre Images")
            
            if len(patient.pre_image_path_list) == 0:
                st.error(":warning: 表示する画像がありません")
            else:
                image_viewer(
                    patient.pre_image_path_list, 
                    ncol=st.session_state.ncol,
                    nrow=st.session_state.nrow, 
                    image_name_visible=is_visible_image_name,
                    key=f"{patient.patient_id}_{condition}_pre")
            
        with post_col:
            st.markdown("## Post Images")
            if len(patient.post_image_path_list) == 0:
                st.error(":warning: 表示する画像がありません")
            else:
                image_viewer(patient.post_image_path_list,
                             ncol=st.session_state.ncol,
                             nrow=st.session_state.nrow,
                             image_name_visible=is_visible_image_name,
                             key=f"{patient.patient_id}_{condition}_post")

if __name__ == '__main__':
    main()
    


