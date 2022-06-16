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
  - [Service Flow](#Service-Flow)

<br>

- [**Demos**](#Demos)

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
**Upccida** 프로젝트의 전반적인 Overview 는 [여기](https://github.com/SOLOv6/solov6-overview)에서 확인이 가능하며, 아래에서는 Flask API 로 구현한 관리자 검수 시스템에 대해 소개합니다.
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

사용자가 차량을 대여하는 시점에 사진을 업로드하면 기본적으로 Event 데이터가 생성됩니다.
이후, 해당 사진에서 차량 파손이 탐지되는 경우에는 **파손 여부**, 모델이 생성한 **마스크 이미지의 경로** 및 모델의 **confidence score** 등의 정보를 포함하는 Entry 데이터가 생성됩니다.
