export type TStateGroup = "backlog" | "unstarted" | "started" | "completed" | "cancelled";
export const issueStateGroupKeys: TStateGroup[] = [
  "backlog",
  "unstarted",
  "started",
  "completed",
  "cancelled",
];

export const filtersPriority: { key: string; title: string }[] = [
  { key: "urgent", title: "Urgent" },
  { key: "high", title: "High" },
  { key: "medium", title: "Medium" },
  { key: "low", title: "Low" },
  { key: "none", title: "None" },
];

export const filterStateGroup: { key: TStateGroup; title: string }[] = [
  { key: "backlog", title: "Backlog" },
  { key: "unstarted", title: "Unstarted" },
  { key: "started", title: "Started" },
  { key: "completed", title: "Completed" },
  { key: "cancelled", title: "Cancelled" },
];

export const filtersStartDate: { key: string; title: string }[] = [
  { key: "last_week", title: "Last Week" },
  { key: "2_weeks_from_now", title: "2 weeks from now" },
  { key: "1_month_from_now", title: "1 month from now" },
  { key: "2_months_from_now", title: "2 months from now" },
  { key: "custom", title: "Custom" },
];

export const filtersDueDate: { key: string; title: string }[] = [
  { key: "last_week", title: "Last Week" },
  { key: "2_weeks_from_now", title: "2 weeks from now" },
  { key: "1_month_from_now", title: "1 month from now" },
  { key: "2_months_from_now", title: "2 months from now" },
  { key: "custom", title: "Custom" },
];

export const displayPropertyGroupBy: { key: string; title: string }[] = [
  { key: "state", title: "States" },
  { key: "state_detail.group", title: "State Groups" },
  { key: "priority", title: "Priority" },
  { key: "Project", title: "Project" }, // required this on my issues
  { key: "labels", title: "Labels" },
  { key: "assignees", title: "Assignees" },
  { key: "created_by", title: "Created By" },
];

export const displayPropertyOrderBy: { key: string; title: string }[] = [
  { key: "sort_order", title: "Manual" },
  { key: "created_at", title: "Last Created" },
  { key: "updated_at", title: "Last Updated" },
  { key: "start_date", title: "Start Date" },
  { key: "priority", title: "Priority" },
];

export const displayPropertyIssueType: { key: string; title: string }[] = [
  { key: "all", title: "All" },
  { key: "active", title: "Active Issues" },
  { key: "backlog", title: "Backlog Issues" },
];

export const displayProperties: { key: string; title: string }[] = [
  { key: "assignee", title: "Assignee" },
  { key: "start_date", title: "Start Date" },
  { key: "due_date", title: "Due Date" },
  { key: "key", title: "ID" },
  { key: "labels", title: "Labels" },
  { key: "priority", title: "Priority" },
  { key: "state", title: "State" },
  { key: "sub_issue_count", title: "Sub Issue Count" },
  { key: "attachment_count", title: "Attachment Count" },
  { key: "link", title: "Link" },
  { key: "estimate", title: "Estimate" },
];

export const extraProperties: { key: string; title: string }[] = [
  { key: "sub_issue", title: "Show sub-issues" }, // in spreadsheet its always false
  { key: "show_empty_groups", title: "Show empty states" }, // filter on front-end
  { key: "calendar_date_range", title: "Calendar Date Range" }, // calendar date range yyyy-mm-dd;before range yyyy-mm-dd;after
  { key: "start_target_date", title: "Start target Date" }, // gantt always be true
];

export const issueFilterVisibilityData: any = {
  my_issues: {
    layout: ["list", "kanban"],
    filters: ["priority", "state_group", "labels", "start_date", "due_date"],
    display_properties: {
      list: true,
      kanban: true,
    },
    display_filters: {
      list: ["group_by", "order_by", "issue_type"],
      kanban: ["group_by", "order_by", "issue_type"],
    },
    extra_options: {
      list: {
        access: true,
        values: ["show_empty_groups"],
      },
      kanban: {
        access: true,
        values: ["show_empty_groups"],
      },
    },
  },
  others: {
    layout: ["list", "kanban", "calendar", "spreadsheet", "gantt"],
    filters: ["priority", "state", "assignees", "created_by", "labels", "start_date", "due_date"],
    display_properties: {
      list: true,
      kanban: true,
      calendar: true,
      spreadsheet: true,
      gantt: false,
    },
    display_filters: {
      list: ["group_by", "order_by", "issue_type", "sub_issue", "show_empty_groups"],
      kanban: ["group_by", "order_by", "issue_type", "sub_issue", "show_empty_groups"],
      calendar: ["issue_type"],
      spreadsheet: ["issue_type"],
      gantt: ["order_by", "issue_type", "sub_issue"],
    },
    extra_options: {
      list: {
        access: true,
        values: ["show_empty_groups", "sub_issue"],
      },
      kanban: {
        access: true,
        values: ["show_empty_groups", "sub_issue"],
      },
      calendar: {
        access: false,
        values: [],
      },
      spreadsheet: {
        access: false,
        values: [],
      },
      gantt: {
        access: true,
        values: ["sub_issue"],
      },
    },
  },
};