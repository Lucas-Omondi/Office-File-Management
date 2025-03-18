import { defineStore } from "pinia";
import api from "../utils/api";

export const useUsersStore = defineStore("users", {
    state: () => ({
        users: [] as any[],
        loading: false,
        error: null as string | null,
    }),

    actions: {
        async fetchUsers() {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get("/users/");
                this.users = response.data;
                console.log("✅ Users fetched successfully", this.users);
            } catch (error: any) {
                this.error = error.response?.data?.detail || "Failed to fetch users";
                console.error("❌ Error fetching users:", this.error);
            } finally {
                this.loading = false;
            }
        },

        async deleteUser(userId: number) {
            try {
                await api.delete(`/users/${userId}/`);
                this.users = this.users.filter(user => user.id !== userId);
                console.log(`🗑️ User ${userId} deleted successfully`);
            } catch (error: any) {
                console.error("❌ Error deleting user:", error.response?.data || error.message);
            }
        },

        async toggleUserStatus(userId: number) {
            const user = this.users.find(u => u.id === userId);
            if (!user) return;

            try {
                const updatedUser = { ...user, is_active: !user.is_active };
                await api.patch(`/users/${userId}/`, { is_active: updatedUser.is_active });
                user.is_active = updatedUser.is_active;
                console.log(`🔄 User ${userId} status updated:`, user.is_active);
            } catch (error: any) {
                console.error("❌ Error updating user status:", error.response?.data || error.message);
            }
        }
    }
});
