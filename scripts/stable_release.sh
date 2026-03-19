#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

cd "${REPO_ROOT}"

banner() {
  printf "${MAGENTA}${BOLD}\n"
  printf "==============================================\n"
  printf "      AB Agency Stable Release Console        \n"
  printf "==============================================\n"
  printf "${RESET}"
}

info() {
  printf "${CYAN}%s${RESET}\n" "$1"
}

success() {
  printf "${GREEN}%s${RESET}\n" "$1"
}

warn() {
  printf "${YELLOW}%s${RESET}\n" "$1"
}

error() {
  printf "${RED}%s${RESET}\n" "$1" >&2
}

require_git_repo() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    error "This script must be run inside a git repository."
    exit 1
  fi
}

create_stable_release() {
  local current_branch stable_stamp stable_tag commit_message

  current_branch=$(git branch --show-current)
  stable_stamp=$(date +"%Y%m%d-%H%M%S")
  stable_tag="stable-${stable_stamp}"
  commit_message="stable: ${stable_stamp}"

  info "Saving the latest stable version from branch '${current_branch}'."
  git add -A

  if git diff --cached --quiet; then
    warn "No new file changes detected. Tagging the current HEAD as a stable version instead."
  else
    git commit -m "${commit_message}"
    success "Committed latest changes as '${commit_message}'."
  fi

  git tag -a "${stable_tag}" -m "Stable release ${stable_tag}"
  success "Created stable tag '${stable_tag}'."

  git push origin "${current_branch}"
  git push origin "${stable_tag}"
  success "Pushed branch '${current_branch}' and tag '${stable_tag}' to origin."
}

rollback_menu() {
  local stable_tags selected_index selected_tag branch_name
  mapfile -t stable_tags < <(git tag --list 'stable-*' --sort=-creatordate)

  if [[ ${#stable_tags[@]} -eq 0 ]]; then
    warn "No historical stable versions are available for rollback."
    return 0
  fi

  printf "${BLUE}${BOLD}\nAvailable Stable Versions${RESET}\n"
  local index=1
  for tag in "${stable_tags[@]}"; do
    printf "${MAGENTA} [%d] ${RESET}%s\n" "${index}" "${tag}"
    index=$((index + 1))
  done

  printf "${MAGENTA} [0] ${RESET}Cancel rollback\n"
  printf "${YELLOW}\nEnter the number of the historical stable version to roll back to: ${RESET}"
  read -r selected_index

  if [[ ! ${selected_index} =~ ^[0-9]+$ ]]; then
    error "Invalid selection. Rollback aborted."
    return 1
  fi

  if [[ ${selected_index} -eq 0 ]]; then
    info "Rollback cancelled. Staying on the current stable version."
    return 0
  fi

  if (( selected_index < 1 || selected_index > ${#stable_tags[@]} )); then
    error "Selection out of range. Rollback aborted."
    return 1
  fi

  selected_tag="${stable_tags[selected_index-1]}"
  branch_name="rollback/${selected_tag}"

  printf "${YELLOW}Roll back to ${selected_tag}? This will switch you to '${branch_name}'. [y/N]: ${RESET}"
  read -r confirm

  if [[ ! ${confirm,,} =~ ^y(es)?$ ]]; then
    info "Rollback cancelled."
    return 0
  fi

  if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
    git switch "${branch_name}"
    git reset --hard "${selected_tag}"
  else
    git switch -c "${branch_name}" "${selected_tag}"
  fi

  success "Rollback branch '${branch_name}' is now checked out at '${selected_tag}'."
  warn "Push the rollback branch manually if you want it published: git push -u origin ${branch_name}"
}

main() {
  banner
  require_git_repo
  create_stable_release

  printf "${YELLOW}\nDo you need further actions? [y/N]: ${RESET}"
  read -r further_actions

  if [[ ${further_actions,,} =~ ^y(es)?$ ]]; then
    rollback_menu
  else
    success "Stable save complete. Goodbye."
    exit 0
  fi

  success "Workflow finished. Goodbye."
}

main "$@"