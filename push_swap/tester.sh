#!/bin/bash
RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

range_start=1
range_end=1000
range_size=100
total_tests=1000
instruction_cap=700
echo "Testing ${range_start} to ${range_end} with size of ${range_size}"
for ((i=1;i<=total_tests;i++)); do
	numbers=$(shuf -i $range_start-$range_end -n ${range_size} | tr '\n' ' ')
	./push_swap $numbers | cat > output
	instruction_count=$(cat output | wc -l)
	checker_status=$(cat output | ./checker_linux $numbers)
	if [[ $instruction_count -ge $instruction_cap ]]; then
		echo "Exceeded treshold of ${instruction_cap}, moves taken: ${instruction_count}"
		echo $numbers
		break
	fi
	if [[ $checker_status == "KO" ]]; then
		echo $numbers
		echo $instruction_count
		echo -e "${RED}${checker_status}${ENDCOLOR}"
		break
	fi
	# echo "Total instructions: ${instruction_count}"
	# echo
	rm -f output
done