export async function enforcePrivacy(userRole: string, location: string, message: any) {
  if (location === "EU" && userRole !== "manager" && message.containsPII) {
    message = { ...message, redacted: true, allergy: undefined, guestInfo: undefined };
  }
  if (userRole && message.allowedRole && userRole !== message.allowedRole) {
    throw new Error("Unauthorized channel access");
  }
  return message;
}