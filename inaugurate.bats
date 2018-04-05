#!/usr/bin/env bats

setup() {
    . "$BATS_TEST_DIRNAME/inaugurate"
}

@test "init vars sets default vars" {
    [ -z "$INAUGURATE_USER" ]
    init_vars
    [ "$INAUGURATE_USER" == "$USER" ]
}
