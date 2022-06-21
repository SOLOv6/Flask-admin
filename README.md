# SOLOv6 Admin Dashboard Overview

<p align="center">
  <img width="319" alt="image" src="https://user-images.githubusercontent.com/85675215/173171356-b5e4092b-ebc7-47b4-bd47-1ac989ee4275.png">
</p>

# INDEX

- [**Introduction**](#Introduction)
  - [Directory](#Directory)
  - [Project Flow](#Project-Flow)

<br>

- [**Admin Dashboard**](#Admin-Dashboard)
  - [Structure](#Structure)
  - [Usecase](#Usecase)
  - [DB ERD](#DB-ERD)

<br>

- [**Demos**](#Demos)
  - [Admin Dashboard Service](#Admin-Dashboard-Service)
  - [Entire Service Flow](#Entire-Service-Flow)

<br>

- [**Tech Stack**](#Tech-Stack)

<br>

# Introduction

**SOLO**(Socar Only Look Once)**v6** 팀은 2022.04.18 ~ 2022.06.08 까지 약 7주 간, **차량 파손 탐지 및 분류 시스템 Upccida** 프로젝트를 진행하였습니다.
<br>
<br>
**Upccida** 는 사용자가 차량을 대여하는 시점에 업로드하는 사진들로부터 **차량의 파손 유무** 및 **파손 종류 분류**, **파손 영역 검출** 등의 Task 를 수행하는 시스템으로,
<br>
웹을 통해 모델의 inference 결과를 Admin Dashboard 에서 관리자가 확인 및 검수하여 최종적으로 보유 차량에 대한 파손 이력 관리가 가능하도록 구현하였습니다.
<br>
<br>
**Upccida** 프로젝트의 전반적인 Overview 는 [여기](https://github.com/SOLOv6/solov6-overview)에서 확인이 가능하며, 아래에서는 Flask API 로 구현한 Admin Dashboard 에 대해 소개합니다.
<br>
<br>

## Directory

### /project

<img width="118" alt="image" src="https://user-images.githubusercontent.com/85675215/173288622-93958118-e49f-4e75-b4d0-bc8e222fbb47.png">

**project** 폴더 내의 디렉터리 구조는 위와 같습니다.

- **\_\_init\_\_.py** : project 패키지의 실행파일로, Flask app 반환
- **apis** : API 패키지
- **configs.py** : CSRF Token, DB Link, Flask 환경 변수 및 설정 파일
- **form** : 관리자 화면의 사용자 인증을 위한 Login & Register Form
- **models** : DB Table 및 각 컬럼에 대한 Scheme 정의
- **routes** : Flask app 에 연결된 각각의 라우팅 경로
- **static** : CSS, JS, Favicon image 와 같은 정적 파일
- **templates** : 각각의 화면을 구성하는 template 파일

<br>

### /project/apis

<img width="117" alt="image" src="https://user-images.githubusercontent.com/85675215/173305362-765e0750-10ee-4dcd-821f-28d14af8309c.png">

<br>

### /project/form

<img width="119" alt="image" src="https://user-images.githubusercontent.com/85675215/173305579-70e6702d-4d7d-4f37-a7e3-26d4c0135970.png">

<br>

### /project/models

<img width="113" alt="image" src="https://user-images.githubusercontent.com/85675215/173306642-fbf9915a-6208-406d-85d7-8c5eed8e0809.png">

<br>

### /project/routes

<img width="138" alt="image" src="https://user-images.githubusercontent.com/85675215/173306895-12cda9b6-1a8a-484b-b146-74e4069c12ba.png">

<br>

### /project/static

<img width="76" alt="image" src="https://user-images.githubusercontent.com/85675215/173307041-b4adde7b-a1f3-4678-bbcf-09ea84d7390c.png">

<br>

### /project/templates

<img width="127" alt="image" src="https://user-images.githubusercontent.com/85675215/173307281-ce10878d-5668-4b6e-9bfc-a31b4486f8ba.png">

<br>
<br>

## Project Flow

<p align="center">
    <img width="971" alt="image" src="https://user-images.githubusercontent.com/85675215/173314826-894827f1-de72-4f20-b52c-219b556335e0.png">
</p>

전체 프로젝트의 **Flow Chart** 는 위와 같습니다.
<br>
크게 **Web**, **Model**, **GCS**, **DB** 로 구분할 수 있으며, 다음과 같은 역할을 수행합니다.
<br>
<br>

### Web

- User 는 차량을 대여하기 전, **6장의 차량 사진을 업로드**합니다.
- Admin Dashboard 에서는 DB 에 저장된 Model 의 **추론 결과 데이터들을 로드하여 랜더링**합니다.

<br>

### Model

- GDC 는 Global Damage Classifier 로, 차량 이미지들을 입력으로 받아 **파손 유무**를 확인합니다.
- 이는 **파손이 탐지되지 않은 차량들을 사전에 선별**하여 이후 모델(LDD)의 부하를 감소시키기 위함입니다.
- GDC 에서 파손이 탐지된 차량 이미지들은 이후 LDD(Local Damage Detector) 모델로 전송되고, **파손 종류 분류 및 파손 영역 검출** Task 를 수행합니다.
- 모든 모델은 **Torch Serve** 를 통해 서빙되며, 모델의 추론 결과는 **Google Cloud Function** 을 통해 DB 에 저장됩니다.

<br>

### GCS

- Google Cloud Storage 는 **실제 이미지들이 저장되는 저장소**입니다.
- User 가 **업로드한 차량 이미지**, LDD 를 통과한 **마스크 이미지** 등이 저장됩니다.
- **HTML Form** 혹은 **Rest API** 를 통해 웹과 통신합니다.
- **GCF**(Google Cloud Function)는 해당 스토리지의 모든 이벤트를 감지하고 있으며, 유저의 업로드 **이벤트가 발생할 경우 Trigger 되는 Function** 입니다.
- **GCF** 를 통해 input 이미지들이 **모델에 순차적으로 입력**되고, 모델의 **추론 결과가 DB 에 저장**됩니다.

<br>

### DB

- DB 는 **MySQL 5.7** 버전을 사용하였습니다.
- **Admin**, **User**, **Car**, **Event**, **Entry** 의 총 5 개 테이블로 이루어져 있습니다.
- Admin Dashboard 에서는 해당 DB 에서 모든 데이터를 로드하고 화면에 랜더링합니다.

<br>

# Admin Dashboard

지금부터는 전체 Project Flow 중 Admin Dashboard 파트에 대해 간단한 설명을 작성하였습니다.

<br>

## Structure

<p align="center">
    <img width="1385" alt="image" src="https://user-images.githubusercontent.com/85675215/174005676-8e8aa5b0-fb3c-4c43-9d73-fe252c8d0e07.png">
</p>

Admin Dashboard 의 구조는 위와 같습니다.

먼저, 웹서버와 Wsgi 는 각각 **Nginx** 와 **Gunicorn** 을 사용하였습니다.
<br>
사내 관리자 검수화면이므로, 거대 트래픽을 처리해야 하는 상황은 없을 것이라고 가정하고 하나의 서버를 두어 구축하였습니다.
<br>

API 프레임워크는 **Flask** 를 사용하였습니다.
<br>
Django 프레임워크도 고려하였으나, 이후 추가할 Mlops 관련 다양한 기술들 간 호환성을 생각해보았을 때, 비교적 커스터마이징 및 세팅에 있어 자유도가 높은 Flask 프레임워크를 선택하였습니다.
<br>
추후에 사용될 기술들이 명확하게 정의되지 않은 상태에서 기술 선택의 제약 및 종속성이 높은 프레임워크를 선택하는 것은 위험하다고 판단하였습니다.
<br>

DB는 **MySQL 5.7** 버전을 사용하였습니다.
<br>
현재로서는 MySQL 의 버전 중 가장 안정적이라고 판단하였으며, 추후 파손 탐지 영역에 대한 Polygon 좌표 값을 배열 형태로 DB 에 담기 위해 PostgreSQL 혹은 mongodb 로 변경할 계획이 있습니다.
<br>

또한, Nginx, Flask, MySQL 은 각각의 **Docker Container** 로 띄워져 **Docker Compose** 로 관리되고 있습니다.
<br>
<br>

## Usecase

<p align="center">
    <img width="873" alt="image" src="https://user-images.githubusercontent.com/85675215/174030273-749a3e65-c4c3-44f8-a5da-e1f85fe371e7.png">
</p>
Admin Dashboard 서비스의 초기 계획된 Usecase 입니다.
<br>

기본적으로 관리자를 위한 서비스인만큼 사용자 인증을 통해 기능을 사용할 수 있도록 구현하였습니다.
<br>
아래에서는 각각의 기능에 대해 정리하였습니다.

- **검색**
  - 보유한 모든 **차량** 검색
  - 등록된 모든 **사용자** 검색
  - 사용자가 차량을 대여한 각각의 **Event** 검색
    - **날짜** 기준 검색
    - 특정 **차량 ID** 기준 검색

<br>

- **추가**
  - **차량** 추가
  - **사용자** 추가

<br>

- **Event 상세 정보 확인(Entry)**

<br>

- **Inspection**

<br>

- **Confirm**

<br>
<br>

### ❗️ **기능 부가 설명**

<br>

#### **Event 상세 정보 확인(Entry)**

> 사용자가 차량을 대여하는 시점에 사진을 업로드하면 기본적으로 Event 데이터가 생성됩니다.
> 이후, 해당 사진에서 차량 파손이 탐지되는 경우에는 **파손 여부**, 모델이 생성한 **마스크 이미지의 경로** 및 모델의 **confidence score** 등의 정보를 포함하는 **Entry 데이터**가 생성됩니다. 이러한 상세 정보는 파손이 탐지된 Event 들에 한해서, 관리자 화면을 통해 직접 확인이 가능합니다.

<br>

#### **Inspection**

> Event 상세 정보 화면에서는 모델이 탐지한 파손 영역을 확인 가능하며, 관리자는 이를 검수 및 확인하여야 합니다. 이 때, 모델이 추론한 파손 영역에 대해 Classification 혹은 Localization 이 잘못 추론되었다고 판단되는 경우에는 관리자가 이를 직접 수정할 수 있습니다. 이는 Inspection 혹은 Annotation 으로 불리며, 관리자가 데이터 라벨링을 수작업으로 진행하는 과정입니다.

<br>

#### **Confirm**

> Event 상세 정보 화면에서 관리자가 모델의 추론 결과 이미지를 확인 및 검수한 결과 이상이 발견되지 않았거나, 이상이 발견된 이미지에 대해 Annotate(Inspect) 가 완료된 이후에는 Confirm 버튼을 클릭하여 최종 검수가 완료되었음을 표시하여야 합니다. Confirm 버튼을 클릭하게 되면, 최종 검수 일자와 로그인된 관리자 계정 이름이 화면에 표시되며 각 이미지에 대한 Annotate(Inspect) 버튼이 비활성화됩니다.

<br>
<br>

## DB ERD

<p align="center">
    <img width="1099" alt="image" src="https://user-images.githubusercontent.com/85675215/174286470-0bba0f88-f3f8-40c0-ae7f-6831bad657c7.png">
</p>

Admin 테이블을 제외한 4 개 테이블의 **객체-관계 다이어그램**입니다.
<br>
각각은 **user_id** 와 **car_id**, **event_id** 로 관계를 맺고 있습니다.
<br>
아래는 테이블의 각 컬럼 명세입니다.
<br>
<br>

### **User**

- **user_name** : 사용자 이름
- **registered_on** : 가입일자 및 시각

### **Car**

- **car_name** : 차량 모델명
- **registered_on** : 등록일자 및 시각

### **Event**

- **user_id** : User 테이블의 기본키(id)
- **car_id** : Car 테이블의 기본키(id)
- **path_original** : 업로드 이미지의 경로
- **created_on** : 대여일자 및 시각
- **is_damaged** : 업로드 이미지에서 검출된 파손 유무
- **conf_score** : 파손 유무에 대한 모델의 confidence score

### **Entry**

- **event_id** : Event 테이블의 기본키(id)
- **is_inferenced** : GDC, LDD 모델 통과 여부(default=True)
- **inferenced_on** : 모델 통과 일자 및 시각
- **path_inference_dent** : 파손 클래스가 "dent" 인 마스크 이미지 경로
- **path_inference_scratch** : 파손 클래스가 "scratch" 인 마스크 이미지 경로
- **path_inference_spacing** : 파손 클래스가 "spacing" 인 마스크 이미지 경로
- **is_inspected** : 관리자의 최종 검수 여부(default=False)
- **inspected_on** : 관리자의 최종 검수 일자 및 시각
- **path_inspect_dent** : 파손 클래스가 "dent" 인 Annotated 마스크 이미지 경로
- **path_inspect_scratch** : 파손 클래스가 "scratch" 인 Annotated 마스크 이미지 경로
- **path_inspect_spacing** : 파손 클래스가 "spacing" 인 Annotated 마스크 이미지 경로
- **inspector** : 최종 검수한 관리자 ID

<br>
<br>

# Demos

구현한 웹서비스의 스크린샷 이미지 및 간단한 시연 영상입니다.

## Admin Dashboard Service

- ### **Login & Register**
  - **세션/쿠키 기반 인증** 방식

<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174506739-e48d07a4-97fe-412c-96de-3ee313e548a5.png">
</p>
<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174506781-5991eb89-2926-4bf1-9208-e2ec78b99307.png">
</p>

<br>

- ### **Events**
  - 네비게이션 바 우측 상단에 **로그인된 관리자 계정** 및 **로그아웃 버튼** 표시
  - **날짜 및 차량 ID 기반 검색** 기능
  - 각 Event 의 **파손 여부** 및 **추론 결과 신뢰도**를 **색상으로 구분**하여 직관적으로 확인 가능
    - **흰색** : 파손이 발견되지 않은 Event
    - **연분홍색** : 파손이 발견되었으며 Model 의 Confidence Score 가 높은 Event
    - **빨간색** : 파손이 발견되었으나 Model 의 Confidence Score 가 낮은 Event
  - 이를 통해 관리자는 **검수 우선순위를 미리 파악**하고, **파손 여부를 인지**함으로서 작업 피로도 감소
  - 각 Event 최우측에 상세 정보 버튼 추가하여 클릭 시 **상세 정보 화면**으로 이동
  - **Pagination 기능** 추가하여 10개 레코드씩 화면에 표시

<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174506980-c4ab28e2-8c92-49d0-a511-2cea491f687d.png">
</p>

<br>

- ### **Cars**
  - 네비게이션 바 우측 상단에 **차량 ID 기준 검색** 기능
  - 차량의 모델명 입력 후 간단하게 **차량 등록** 가능
  - 삭제 버튼 추가하여 간단하게 **차량 삭제** 가능
  - **Pagination 기능** 추가하여 10개 레코드씩 화면에 표시

<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174508886-991fd74c-39ae-4aca-b621-3c498d2d4931.png">
</p>

<br>

- ### **Users**
  - 네비게이션 바 우측 상단에 **사용자 ID 기준 검색** 기능
  - 사용자 이름 입력 후 간단하게 **사용자 등록** 가능
  - 삭제 버튼 추가하여 간단하게 **사용자 삭제** 가능
  - **Pagination 기능** 추가하여 10개 레코드씩 화면에 표시

<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174509255-6524614e-c01f-474d-b9c3-b5a66fcc7585.png">
</p>

<br>

- ### **Event 상세 정보(Entry)**
  - Event Page 에서 상세 정보 버튼 클릭하여 **개별 Event 상세 정보 확인** 가능
  - 선택한 **Event 의 ID**, **대여 날짜 및 시각**, **대여한 사용자**, **차량** 등의 정보 표시
  - 업로드된 차량 이미지 전체에 대해 **모델이 탐지한 파손 클래스 및 파손 영역이 마스킹**되어 표시
  - 이미지 각각에 대해 **파손 여부 표시** (is_damaged)
    - dent, scratch, spacing 클래스 중 **하나의 클래스에서라도 파손이 탐지된다면 True**
    - dent, scratch, spacing 클래스 중 **어떤 클래스에서도 파손이 탐지되지 않았다면 False**
  - 관리자가 파손 클래스 및 파손 영역 마스크를 확인 후 **오류를 발견**하였다면, <br> **inspect 버튼을 클릭**하여 직접 **Annotate** 가능
  - 해당 Event 에 대한 **모든 검수 작업이 종료**되면, **최종 검수 확인 버튼**(Confirmed!)을 클릭
  - **최종 검수가 완료**되면, **검수자**(현재 관리자 계정 ID) 및 **검수 완료 일자 및 시각**이 저장되고 화면에 표시, inspect 버튼 비활성화

<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174509898-bf1faf3e-c59b-4f72-8c93-ad44268723bd.png">
</p>
<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174510004-e5c21f00-d575-4145-9aeb-b67aa6f0b285.png">
</p>

<br>

- ### **Annotate**
  - Event 상세 정보 화면에서 **inspect 버튼을 클릭**하면 **라벨링 화면으로 이동**
  - **VGG Image Annotator(VIA)** 툴의 코드를 일부 수정하여 사용
    - 수정을 원하는 **원본 이미지를 자동으로 load**
    - dent, scratch, spacing **3개 클래스 자동으로 load**
  - 라벨링 작업이 완료되면, **json 파일로 저장**
    - 해당 파일은 각 클래스에 대한 **Polygon 좌표값**
  - 좌표값을 읽어 **새로운 마스크 이미지를 생성**하고 **모델 재학습** 가능

<p align="center">
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/85675215/174512488-c7f3f9aa-dd6e-41b6-8328-93d11c657766.png">
</p>

<br>
<br>

## Entire Service Flow

전체 프로젝트의 짧은 시연 영상입니다.
<br>
영상은 **사용자의 차량 사진 업로드**부터 **관리자 검수 완료**까지 전체적인 Flow 를 담고 있습니다.
<br>
<br>

- ### **User Upload**
  ![user-upload](/demos/user-upload.gif)

<br>

- ### **Logs**
  ![logs](/demos/cloud_func-database.gif)

<br>

- ### **Admin Dashboard - Login & Tabs**
  ![event](/demos/event.gif)

<br>

- ### **Admin Dashboard - Event details**
  ![entry_1](/demos/entry_1.gif)
  ![entry_2](/demos/entry_2.gif)

<br>

- ### **Admin Dashboard - Annotate**
  ![annotate](/demos/annotate.gif)

<br>
<br>

# Tech Stack

Admin Dashboard 구현에 활용된 기술들의 Tech Stack 입니다.

<br>

- ### Languages
<img src='https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white'/> <img src='https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white'/> <img src='https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white'/>

<br>

- ### Frameworks & Libraries
<img src='https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white'/> <img src='https://img.shields.io/badge/Jinja Templates-B41717?style=for-the-badge&logo=Jinja&logoColor=white'/> <img src='https://img.shields.io/badge/SqlAlchemy-C11920?style=for-the-badge&logo=Swiper&logoColor=white'/> <img src='https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=Bootstrap&logoColor=white'/>

<br>

- ### DB
<img src='https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white'/> <img src='https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=E48E01'/>

<br>

- ### Deployment & Tools
<img src='https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white'/> <img src='https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=AmazonAWS&logoColor=F0921E'/> <img src='https://img.shields.io/badge/Google_Cloud_Platform-4285F4?style=for-the-badge&logo=GoogleCloud&logoColor=white'/>
