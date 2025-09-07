export async function enforcePrivacy(userRole, location, message) {
  // ...existing checks
  // Audit log example
  console.log(`[AUDIT] User ${userRole} accessed ${JSON.stringify(message)} in ${location} at ${new Date().toISOString()}`);
  return message;
}