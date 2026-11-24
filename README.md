# Codex Playbook

Xcode와 Swift를 사용하는 iOS 개발을 중심으로, Codex의 작업 원칙과 재사용 가능한 스킬을 모은 플레이북입니다.
Android와 크로스·멀티 플랫폼 작업에서는 해당 프로젝트의 기술과 관례를 따릅니다.

- [한국어 지침](./AGENTS.ko.md) — 제가 사용하는 기본 버전
- [English instructions](./AGENTS.en.md) — 같은 지침의 영어 버전

## 구성

```text
codex-playbook/
├── README.md
├── AGENTS.ko.md
├── AGENTS.en.md
└── skills/
    ├── swift-change-review/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── collect_changes.py
    │   └── references/
    │       └── concurrency-review.md
    └── ios-mr-preflight/
        ├── SKILL.md
        └── references/
            ├── mr-writing-guide.md
            ├── manual-verification.md
            └── mr-template.md
```

`AGENTS.md`에는 기본 작업 원칙을, 각 스킬에는 특정 업무의 절차를 둡니다. 상세 기준과 템플릿은 `references/`에서 필요할 때 읽고, 반복 가능한 정보 수집은 `scripts/`로 처리합니다.

### Swift 변경 코드 리뷰

[swift-change-review](./skills/swift-change-review/SKILL.md)는 Swift 변경 코드에서 의도와 다른 동작이나 기존 기능의 회귀를 찾습니다.

- [변경 수집 스크립트](./skills/swift-change-review/scripts/collect_changes.py): 스테이징·미스테이징·미추적·충돌 파일 목록을 JSON으로 출력합니다. 파일 내용이나 저장소를 수정하지 않습니다.
- [동시성 검토 기준](./skills/swift-change-review/references/concurrency-review.md): 관련 변경이 있을 때 actor 격리, 작업 취소와 객체 수명을 확인합니다.

스크립트에는 Git과 Python 3.9 이상이 필요하며 추가 Python 패키지는 필요하지 않습니다. 이 도구는 현재 작업 트리 목록 수집용입니다. 브랜치·커밋·PR 비교는 사용자가 지정한 diff 범위를 따릅니다.

### iOS PR/MR 제출 전 점검

[ios-mr-preflight](./skills/ios-mr-preflight/SKILL.md)는 브랜치 변경 내용을 검토하고, 한국어 PR/MR 설명 초안과 수동 검증 체크리스트를 작성합니다.

- [MR 작성 기준](./skills/ios-mr-preflight/references/mr-writing-guide.md): 변경 이유, 변경 후 동작, 비교 범위와 검토 결과 작성법
- [수동 검증 기준](./skills/ios-mr-preflight/references/manual-verification.md): 조건·행동·기대 결과 및 검증 상태 작성법
- [기본 PR/MR 템플릿](./skills/ios-mr-preflight/references/mr-template.md): 저장소 자체 템플릿이 없을 때 사용하는 양식

템플릿은 **저장소의 PR/MR 템플릿 → 스킬의 기본 템플릿** 순서로 선택합니다. 전역 `AGENTS.md`에는 템플릿을 중복 보관하지 않습니다.

## 주요 작업 원칙

- 기존 구현과 호출 흐름을 파악한 뒤, 프로젝트의 구조와 코딩 스타일을 유지하면서 필요한 범위만 수정합니다.
- 기본 검증은 정적 코드 검토로 진행합니다. 빌드, 테스트, 커밋, 푸시, 새 의존성 추가는 각각 명시적으로 요청한 경우에만 수행합니다.
- 의미 있는 코드 변경 후에는 커밋 메시지를 제안합니다. iOS PR/MR 작성과 제출 전 점검은 `ios-mr-preflight`의 절차를 따릅니다.
- 기본 응답은 한국어로 작성하고, 코드 식별자와 API 이름은 원문을 유지합니다.

## 적용 방법

### 1. 저장소 다운로드

```bash
git clone https://github.com/RaeBaek/codex-playbook.git
cd codex-playbook
```

### 2. 전역 지침 적용

KR·EN 중 하나를 골라 Codex의 전역 지침 파일인 `~/.codex/AGENTS.md`에 내용을 복사합니다. 이미 전역 지침을 사용 중이라면 기존 내용을 백업하거나 필요한 규칙을 합쳐서 저장하세요.

두 버전 모두 기본 응답 언어는 한국어입니다. EN은 지침 본문을 영어로 옮긴 버전입니다. `CODEX_HOME`을 별도로 설정했다면 해당 디렉터리 기준으로 경로를 조정하세요.

### 3. 스킬 설치

`skills/` 아래의 각 스킬 폴더를 **하위 파일 전체와 함께** `~/.codex/skills/`에 복사합니다. 이미 같은 이름의 스킬이 있다면 백업 후 변경 내용을 비교하여 반영하세요.

기본 경로를 사용하며, 기존 파일을 덮어써도 되는지 확인한 경우 저장소 루트에서 다음 명령으로 두 스킬을 복사할 수 있습니다.

```bash
mkdir -p ~/.codex/skills
cp -R skills/swift-change-review ~/.codex/skills/
cp -R skills/ios-mr-preflight ~/.codex/skills/
```

`SKILL.md`만 복사하면 참고 문서와 스크립트의 연결이 끊어집니다. 전역 지침이 `ios-mr-preflight`를 참조하므로 해당 스킬도 함께 설치하세요.

### 4. 새 채팅에서 사용

새 Codex 채팅을 열고 적용된 지침을 확인합니다.

```text
현재 적용된 전역 지침과 프로젝트 지침을 구분해서 알려줘.
빌드, 테스트, 커밋, 의존성 추가는 각각 어떤 조건에서 수행하는지도 설명해줘.
```

개인 작업 방식은 전역 파일에 두고, 팀 코딩 규칙이나 프로젝트 고유의 구조는 해당 저장소의 `AGENTS.md`에서 관리할 수 있습니다.

스킬을 명시적으로 선택하려면 다음과 같이 요청합니다.

```text
$swift-change-review 현재 작업 트리의 Swift 변경을 리뷰해 줘.
```

```text
$ios-mr-preflight 기준 브랜치는 main이야. 현재 브랜치의 PR 설명 초안과 수동 검증 항목을 작성해 줘.
```

`main`은 예시입니다. 실제 저장소에서 사용하는 기준 브랜치를 지정하세요. 자연어 요청으로도 스킬이 선택될 수 있지만, 확실하게 선택하려면 이름을 명시하세요. 스킬 호출 자체가 파일 수정, 빌드·테스트 실행, MR 게시를 허용하는 것은 아닙니다.

이 저장소는 지침과 스킬을 파일로 복사해 사용하는 구성입니다. 설치 스크립트나 플러그인 마켓플레이스는 포함하지 않습니다.
