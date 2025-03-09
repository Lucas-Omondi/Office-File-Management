import { defineStore } from "pinia";
import { ref } from "vue";

interface Project {
    id: number;
    name: string;
}

export const useProjectStore = defineStore("projectStore", () => {
    const selectedProjects = ref<Project[]>([]);

    const addSelectedProject = (project: Project) => {
        selectedProjects.value.push(project);
    };

    const removeSelectedProjects = () => {
        selectedProjects.value = [];
    };

    return {
        selectedProjects,
        addSelectedProject,
        removeSelectedProjects,
    };
});
