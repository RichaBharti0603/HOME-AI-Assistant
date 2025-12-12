// frontend/next-app/utils/user.js
export function getUserId() {
  if (typeof window === "undefined") return "user_server"; // SSR safety
  let id = localStorage.getItem("home_user_id");
  if (!id) {
    id = "user_" + Date.now();
    localStorage.setItem("home_user_id", id);
  }
  return id;
}

export function clearUserId() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("home_user_id");
}
