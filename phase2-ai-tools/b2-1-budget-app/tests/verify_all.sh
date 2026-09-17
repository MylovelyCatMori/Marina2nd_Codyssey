#!/usr/bin/env bash
# Phase 6 최종 검증. 명령 12개의 정상/오류 경로와 종료 코드를 한 번에 확인한다.
# 실행: bash tests/verify_all.sh   (프로젝트 루트에서)
set -u

DATA=verify-data
OUT=verify-out
rm -rf "$DATA" "$OUT"
mkdir -p "$OUT"

ok=0
fail=0

run() { # 설명 기대종료코드 명령...
  local name="$1" expect="$2"
  shift 2
  "$@" > "$OUT/last.txt" 2>&1
  local code=$?
  if [ "$code" = "$expect" ]; then
    ok=$((ok + 1))
    printf 'OK   [%s] %s\n' "$code" "$name"
  else
    fail=$((fail + 1))
    printf 'FAIL [got %s, want %s] %s\n' "$code" "$expect" "$name"
    sed 's/^/       /' "$OUT/last.txt"
  fi
}

app() { python -m budget_app --data-dir "$DATA" "$@"; }

# 대화형 add 는 표준 입력으로 값을 밀어 넣는다
add_tx() { # 날짜 타입 카테고리 금액 메모 태그
  printf '%s\n%s\n%s\n%s\n%s\n%s\n' "$1" "$2" "$3" "$4" "$5" "$6" | app add
}

echo "== --help =="
for c in "" add list update delete search summary budget category export import backup recurring; do
  run "--help ${c:-(최상위)}" 0 python -m budget_app $c --help
done

echo
echo "== 정상 경로 =="
run "add 수입"        0 bash -c 'printf "2024-01-05\nincome\nsalary\n3000000\n1월 월급\nfixed\n" | python -m budget_app --data-dir '"$DATA"' add'
run "add 지출(쉼표 메모)" 0 bash -c 'printf "2024-01-12\nexpense\nfood\n8000\n김밥, 라면\nmeal, quick\n" | python -m budget_app --data-dir '"$DATA"' add'
run "add 지출2"       0 bash -c 'printf "2024-01-25\nexpense\ntransport\n50000\n교통카드\n\n" | python -m budget_app --data-dir '"$DATA"' add'
run "list"            0 app list --limit 5
run "search 기간"      0 app search --from 2024-01-01 --to 2024-01-31
run "search 조건조합"   0 app search --category food --type expense --q 김밥 --tag quick
run "budget set"      0 app budget set --month 2024-01 --amount 50000
run "summary"         0 app summary --month 2024-01 --top 3
run "summary 빈 달"    0 app summary --month 2023-12
run "category list"   0 app category list
run "category add"    0 app category add --name cafe
run "category remove(미사용)" 0 app category remove --name cafe
run "export month"    0 app export --out "$OUT/jan.csv" --month 2024-01
run "export 기간"      0 app export --out "$OUT/range.csv" --from 2024-01-01 --to 2024-01-31
run "import"          0 app import --from "$OUT/jan.csv"
run "backup"          0 app backup
run "recurring add"   0 app recurring add --day 25 --type income --category salary --amount 3000000 --memo 월급
run "recurring list"  0 app recurring list
run "recurring apply" 0 app recurring apply --month 2024-02
run "recurring apply 재실행(중복 방지)" 0 app recurring apply --month 2024-02
run "recurring remove" 0 app recurring remove --id RC-0001
run "update(수정 없음)" 0 bash -c 'printf "0\n" | python -m budget_app --data-dir '"$DATA"' update --id TX-000001'
run "delete"          0 app delete --id TX-000001

echo
echo "== 오류 경로 (종료 코드 1) =="
run "list --limit 0"        1 app list --limit 0
run "summary 잘못된 월"       1 app summary --month 2024-13
run "summary --top 0"       1 app summary --month 2024-01 --top 0
run "update 없는 id"         1 app update --id NOPE
run "delete 없는 id"         1 app delete --id NOPE
run "search 없는 카테고리"     1 app search --category nope
run "budget 잘못된 금액"       1 app budget set --month 2024-01 --amount -5
run "budget 하위명령 없음"     1 app budget
run "category remove 사용 중"  1 app category remove --name food
run "category remove 없는 이름" 1 app category remove --name nope
run "category add 중복"       1 app category add --name food
run "category 하위명령 없음"   1 app category
run "export 조건 누락"        1 app export --out "$OUT/bad.csv"
run "import 없는 파일"        1 app import --from "$OUT/nope.csv"
run "recurring day 31"      1 app recurring add --day 31 --type expense --category rent --amount 500000
run "recurring remove 없는 id" 1 app recurring remove --id RC-9999
run "recurring 하위명령 없음"  1 app recurring

# 헤더가 다른 CSV
printf '날짜,금액\n2024-03-01,100\n' > "$OUT/wrong.csv"
run "import 헤더 불일치"      1 app import --from "$OUT/wrong.csv"

echo
echo "== 스택트레이스 검사 =="
if grep -rl "Traceback" "$OUT" > /dev/null 2>&1; then
  fail=$((fail + 1))
  echo "FAIL 스택트레이스가 출력됐다"
else
  ok=$((ok + 1))
  echo "OK   스택트레이스 0건"
fi

echo
echo "통과 $ok / 실패 $fail"
rm -rf "$DATA" "$OUT"
[ "$fail" = 0 ]
