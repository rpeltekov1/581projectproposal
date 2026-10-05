CREATE TABLE `members` (
	`user_id` text PRIMARY KEY NOT NULL,
	`email` text NOT NULL,
	`role` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `plans` (
	`id` text PRIMARY KEY NOT NULL,
	`owner` text NOT NULL,
	`filename` text NOT NULL,
	`object_key` text NOT NULL,
	`sha256` text NOT NULL,
	`mime` text NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_plans_owner` ON `plans` (`owner`);--> statement-breakpoint
CREATE TABLE `published` (
	`id` text PRIMARY KEY NOT NULL,
	`review_id` text NOT NULL,
	`owner` text NOT NULL,
	`details` text NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `reviews` (
	`id` text PRIMARY KEY NOT NULL,
	`run_id` text NOT NULL,
	`owner` text NOT NULL,
	`result` text NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_reviews_run` ON `reviews` (`run_id`);--> statement-breakpoint
CREATE TABLE `runs` (
	`id` text PRIMARY KEY NOT NULL,
	`plan_id` text NOT NULL,
	`owner` text NOT NULL,
	`status` text NOT NULL,
	`version` text NOT NULL,
	`mode` text NOT NULL,
	`result` text,
	`provenance` text,
	`error` text,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_runs_owner_created` ON `runs` (`owner`,`created`);--> statement-breakpoint
CREATE TABLE `scores` (
	`id` text PRIMARY KEY NOT NULL,
	`run_id` text NOT NULL,
	`owner` text NOT NULL,
	`key_hash` text NOT NULL,
	`answer_key` text NOT NULL,
	`metrics` text NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_scores_owner` ON `scores` (`owner`);