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
├── plugin.json
├── .agents/
│   └── plugins/
│       └── marketplace.json
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

### 3. 플러그인 설치 (권장)

두 스킬과 부속 파일을 `ios-dev-playbook` 플러그인으로 함께 설치할 수 있습니다. `codex plugin` 명령을 지원하는 Codex CLI가 필요합니다.

저장소를 내려받은 폴더에서 로컬 마켓플레이스를 등록하고 설치합니다.

```bash
codex plugin marketplace add .
codex plugin add ios-dev-playbook@codex-playbook
```

플러그인 설정이 GitHub에 반영된 뒤에는 팀원이 저장소 경로 대신 GitHub 주소로 등록할 수도 있습니다.

```bash
codex plugin marketplace add RaeBaek/codex-playbook
codex plugin add ios-dev-playbook@codex-playbook
```

위 두 등록 방식 중 하나를 선택하세요. 로컬 경로 등록은 해당 폴더를 유지해야 하며, GitHub 등록은 원격에 반영된 파일을 사용합니다.

설치 상태는 다음 명령으로 확인합니다.

```bash
codex plugin list --marketplace codex-playbook
```

설치 후 새 채팅 또는 새 CLI 세션을 시작하세요. CLI의 `/plugins`에서도 플러그인을 확인할 수 있습니다. 이 플러그인은 별도의 MCP 서버 연결이나 API 키가 필요하지 않습니다. Git, Python 등 기존 스크립트 실행 환경은 별도로 필요합니다.

`AGENTS.ko.md`와 `AGENTS.en.md`는 배포용 지침 문서입니다. 플러그인을 설치해도 개인 전역 `AGENTS.md`를 자동으로 덮어쓰지 않으므로 전역 지침은 2단계에서 별도로 적용하세요.

### 스킬 폴더 직접 복사 (대안)

플러그인 설치와 직접 복사 중 한 방식을 선택하세요. 이미 직접 설치한 같은 이름의 스킬이 있다면 중복될 수 있으므로 새 채팅에서 실제 선택된 스킬의 경로를 확인하세요. 기존 스킬은 자동 삭제하지 않습니다.

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

직접 복사한 스킬을 명시적으로 선택하려면 다음과 같이 요청합니다. 플러그인 설치 시에는 플러그인을 선택하거나 “ios-dev-playbook 플러그인의 Swift 변경 코드 리뷰 스킬을 사용해 줘”처럼 요청하고, 선택된 스킬 경로가 해당 플러그인의 설치 경로인지 확인하세요.

```text
$swift-change-review 현재 작업 트리의 Swift 변경을 리뷰해 줘.
```

```text
$ios-mr-preflight 기준 브랜치는 main이야. 현재 브랜치의 PR 설명 초안과 수동 검증 항목을 작성해 줘.
```

`main`은 예시입니다. 실제 저장소에서 사용하는 기준 브랜치를 지정하세요. 자연어 요청으로도 스킬이 선택될 수 있지만, 확실하게 선택하려면 이름을 명시하세요. 스킬 호출 자체가 파일 수정, 빌드·테스트 실행, MR 게시를 허용하는 것은 아닙니다.

## 플러그인 구성과 업데이트

- [plugin.json](./plugin.json): `ios-dev-playbook`의 이름, 버전과 표시 정보
- [marketplace.json](./.agents/plugins/marketplace.json): `codex-playbook` 설치 목록. `source.path`는 저장소 루트의 `./`를 가리킵니다.
- `skills/`: 기존 두 스킬과 스크립트·참고 문서를 그대로 사용합니다.

GitHub 마켓플레이스의 최신 내용을 가져오려면 다음을 실행합니다.

```bash
codex plugin marketplace upgrade codex-playbook
```

이 명령은 Git 기반 마켓플레이스의 스냅샷을 갱신합니다. 플러그인 설치 상태를 확인하고, 설치된 사본이 이전 내용이라면 플러그인 브라우저에서 다시 설치한 뒤 새 채팅에서 확인하세요. 로컬 경로 등록은 원본 폴더를 갱신한 뒤 설치된 사본을 갱신해야 합니다. 설치 캐시를 직접 수정하지 마세요.

플러그인을 제거하려면 다음을 실행합니다. 직접 복사한 스킬이나 전역 지침은 별도로 유지됩니다.

```bash
codex plugin remove ios-dev-playbook@codex-playbook
```

이 저장소의 마켓플레이스는 팀 배포용 목록이며, OpenAI 공개 플러그인 디렉터리에 게시하는 절차와는 별개입니다. 설치 스크립트는 포함하지 않습니다.

- [OpenAI 플러그인 패키징 및 마켓플레이스 공식 문서](https://developers.openai.com/plugins/build/plugins)
