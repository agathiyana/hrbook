CREATE TABLE IF NOT EXISTS requirement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requirementname String NOT NULL,
    clientname String NOT NULL,
    clientmanager String NOT NULL,
	departmentname String NOT NULL,
	accountmanager String NOT NULL,
	jobdescription String NOT NULL,
	workexperience String NOT NULL,
	openposition String NOT NULL,
	startdate String NOT NULL,
	enddate String NOT NULL,
	display String NOT NULL,
	jobstatus String NOT NULL
);