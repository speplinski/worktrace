# Leave-one-out robustness (exploratory, common core)

Each line removes one intervention type or one configuration and recomputes: the registered H3 mixed model (one-sided p, DSA vs track record), H3 cell counts DSA better:worse against each rule, and how many interventional basis failures the LLM procedure audit passes.


## Primary

- all: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 68% of 474 wrong-basis, flags 17% of good
- drop arm add_Y: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 68% of 441 wrong-basis, flags 18% of good
- drop arm add_Y_remove_X: GLMM p=0.0 | vs judged process: 11:0; vs judged grounds: 13:0; vs track record: 9:0 | judge passes 68% of 454 wrong-basis, flags 17% of good
- drop arm invert_X: GLMM p=0.004 | vs judged process: 11:0; vs judged grounds: 14:1; vs track record: 8:0 | judge passes 67% of 363 wrong-basis, flags 18% of good
- drop arm only_X: GLMM p=0.0 | vs judged process: 11:0; vs judged grounds: 13:0; vs track record: 9:0 | judge passes 68% of 460 wrong-basis, flags 17% of good
- drop arm remove_X: GLMM p=0.381 | vs track record: 3:4; vs judged process: 7:1; vs judged grounds: 9:1 | judge passes 61% of 298 wrong-basis, flags 18% of good
- drop basal:basal-2.0-max: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 68% of 474 wrong-basis, flags 17% of good
- drop claude:claude-haiku-5-5:medium: GLMM p=0.0 | vs track record: 9:0; vs judged process: 10:0; vs judged grounds: 12:0 | judge passes 67% of 439 wrong-basis, flags 17% of good
- drop claude:claude-opus-5-5:medium: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 11:0 | judge passes 67% of 455 wrong-basis, flags 19% of good
- drop claude:claude-sonnet-5-5:medium: GLMM p=0.0 | vs track record: 8:0; vs judged process: 9:0; vs judged grounds: 11:0 | judge passes 66% of 439 wrong-basis, flags 18% of good
- drop ollama-inline:SpeakLeash/bielik-11b-v3.0-instruct:Q8_0:seed7: GLMM p=0.003 | vs track record: 8:0; vs judged process: 10:0; vs judged grounds: 13:0 | judge passes 71% of 419 wrong-basis, flags 15% of good
- drop ollama:gemma4:26b:seed7:default: GLMM p=0.0 | vs track record: 9:0; vs judged process: 10:0; vs judged grounds: 12:0 | judge passes 70% of 428 wrong-basis, flags 18% of good
- drop ollama:gpt-oss:120b:seed7:default: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 70% of 404 wrong-basis, flags 16% of good
- drop ollama:mistral-small3.2:24b:seed7:default: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 72% of 414 wrong-basis, flags 16% of good
- drop ollama:qwen3.8:27b:seed7:default: GLMM p=0.002 | vs track record: 7:0; vs judged process: 9:0; vs judged grounds: 11:0 | judge passes 66% of 435 wrong-basis, flags 16% of good
- drop openai-decisions:gpt-6-luna: GLMM p=0.0 | vs track record: 9:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 68% of 474 wrong-basis, flags 17% of good
- drop openai:gpt-6-luna:medium: GLMM p=0.0 | vs track record: 8:0; vs judged process: 10:0; vs judged grounds: 12:0 | judge passes 66% of 430 wrong-basis, flags 19% of good
- drop openai:gpt-6.1-sol:medium: GLMM p=0.004 | vs track record: 7:0; vs judged process: 9:0; vs judged grounds: 11:0 | judge passes 66% of 449 wrong-basis, flags 19% of good
- drop openai:gpt-6.1-terra:medium: GLMM p=0.001 | vs track record: 8:0; vs judged process: 10:0; vs judged grounds: 11:0 | judge passes 65% of 428 wrong-basis, flags 19% of good
- drop systemone:d1: GLMM p=0.0 | vs track record: 8:0; vs judged process: 11:0; vs judged grounds: 13:0 | judge passes 68% of 474 wrong-basis, flags 17% of good

## Without contested arms (A1)

- all: GLMM p=0.193 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 59% of 288 wrong-basis, flags 17% of good
- drop arm add_Y: GLMM p=0.193 | vs track record: 4:3; vs judged process: 7:1; vs judged grounds: 9:1 | judge passes 57% of 255 wrong-basis, flags 18% of good
- drop arm add_Y_remove_X: GLMM p=0.113 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 58% of 267 wrong-basis, flags 18% of good
- drop arm invert_X: GLMM p=0.727 | vs judged process: 6:1; vs judged grounds: 9:2; vs track record: 2:3 | judge passes 56% of 212 wrong-basis, flags 18% of good
- drop arm only_X: GLMM p=0.128 | vs judged process: 7:0; vs judged grounds: 9:1; vs track record: 4:2 | judge passes 59% of 269 wrong-basis, flags 18% of good
- drop arm remove_X: GLMM p=0.215 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 3:3 | judge passes 59% of 244 wrong-basis, flags 18% of good
- drop basal:basal-2.0-max: GLMM p=0.184 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 59% of 288 wrong-basis, flags 17% of good
- drop claude:claude-haiku-5-5:medium: GLMM p=0.193 | vs judged process: 6:1; vs judged grounds: 8:1; vs track record: 4:3 | judge passes 58% of 267 wrong-basis, flags 17% of good
- drop claude:claude-opus-5-5:medium: GLMM p=0.193 | vs judged process: 7:1; vs judged grounds: 7:1; vs track record: 4:3 | judge passes 58% of 283 wrong-basis, flags 19% of good
- drop claude:claude-sonnet-5-5:medium: GLMM p=0.199 | vs judged process: 5:1; vs judged grounds: 7:1; vs track record: 3:3 | judge passes 58% of 279 wrong-basis, flags 19% of good
- drop ollama-inline:SpeakLeash/bielik-11b-v3.0-instruct:Q8_0:seed7: GLMM p=0.478 | vs judged process: 6:1; vs judged grounds: 9:1; vs track record: 3:3 | judge passes 63% of 234 wrong-basis, flags 16% of good
- drop ollama:gemma4:26b:seed7:default: GLMM p=0.059 | vs judged process: 6:0; vs judged grounds: 8:0; vs track record: 4:2 | judge passes 59% of 267 wrong-basis, flags 17% of good
- drop ollama:gpt-oss:120b:seed7:default: GLMM p=0.183 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 60% of 225 wrong-basis, flags 16% of good
- drop ollama:mistral-small3.2:24b:seed7:default: GLMM p=0.185 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 63% of 234 wrong-basis, flags 16% of good
- drop ollama:qwen3.8:27b:seed7:default: GLMM p=0.315 | vs judged process: 6:1; vs judged grounds: 8:1; vs track record: 3:3 | judge passes 58% of 276 wrong-basis, flags 17% of good
- drop openai-decisions:gpt-6-luna: GLMM p=0.188 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 59% of 288 wrong-basis, flags 17% of good
- drop openai:gpt-6-luna:medium: GLMM p=0.174 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 4:3 | judge passes 57% of 268 wrong-basis, flags 19% of good
- drop openai:gpt-6.1-sol:medium: GLMM p=0.095 | vs judged process: 6:1; vs judged grounds: 8:1; vs track record: 4:1 | judge passes 58% of 283 wrong-basis, flags 19% of good
- drop openai:gpt-6.1-terra:medium: GLMM p=0.179 | vs judged process: 7:1; vs judged grounds: 8:1; vs track record: 4:3 | judge passes 56% of 264 wrong-basis, flags 19% of good
- drop systemone:d1: GLMM p=0.413 | vs judged process: 7:1; vs judged grounds: 9:1; vs track record: 3:3 | judge passes 59% of 288 wrong-basis, flags 17% of good
