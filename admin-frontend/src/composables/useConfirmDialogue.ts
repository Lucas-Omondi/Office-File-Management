import { createApp, ref } from "vue";
import ConfirmDialog from "../components/ConfirmDialogue.vue"; // 🔥 Create this component

export function useConfirmDialog(title: string, message: string): Promise<boolean> {
    return new Promise((resolve) => {
        const dialogVisible = ref(false);

        const confirm = () => {
            resolve(true);
            dialogVisible.value = false;
            app.unmount();
            document.body.removeChild(container);
        };

        const cancel = () => {
            resolve(false);
            dialogVisible.value = false;
            app.unmount();
            document.body.removeChild(container);
        };

        const container = document.createElement("div");
        document.body.appendChild(container);

        const app = createApp(ConfirmDialog, { title, message, visible: dialogVisible, confirm, cancel });
        app.mount(container);

        dialogVisible.value = true;
    });
}
