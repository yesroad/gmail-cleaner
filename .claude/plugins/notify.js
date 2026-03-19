import { $ } from "bun"

// OpenCode 알림 플러그인
// permission.asked 이벤트 시 macOS 알림 발송 (terminal-notifier 필요)
export default () => ({
  "permission.asked": async () => {
    await $`terminal-notifier -title OpenCode -message "확인이 필요합니다" -sound Glass`.nothrow()
    process.stdout.write("\u0007")
  },
})
