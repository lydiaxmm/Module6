// Demo Extensible Calendar App
// Created for CSE 330S by Shane Carr
// Washington University in St. Louis
 
 
// Ext.JS wants you to use `Ext.define` when making a custom component.
Ext.define("CSE330.Calendar", {
 
	// List the classes we use inside this component.  This enables Ext.JS to load
	// the files containing the definitions for these classes more efficiently.
	requires: [],
 
	// Main code for our component
	constructor: function(){
		// Set up the calendar store
		this.calendarStore = Ext.create("Extensible.calendar.data.MemoryCalendarStore", {
			autoLoad: true,
			storeId: "Calendars",
			proxy: {
				type: "rest",
				url: "/cal/",
				startParam: "offset",
				reader: {
					type: "json",
					root: "objects"
				},
				writer: {
					type: "json",
					nameProperty: "mapping"
				}
			}
		});
 
		// Set up the event store
		this.eventStore = Ext.create("Extensible.calendar.data.MemoryEventStore", {
			autoLoad: true,
			storeId: "Events",
			proxy: {
				type: "rest",
				url: "/event/",
				startParam: "offset",
				reader: {
					type: "json",
					root: "objects",
				},
				writer: {
					type: "json",
					nameProperty: "mapping"
				}
			}
		});
 
		// Set up the panel (view)
		this.container = Ext.create('Extensible.calendar.CalendarPanel', {
			renderTo: Ext.get("calbox"),
			title: "My CSE330 Calendar",
			width: "100%",
			height: "100%",
			id: "ext-calendar-main",
			eventStore: this.eventStore,
			calendarStore: this.calendarStore,
			monthViewCfg: {
				showHeader: true // show the days of the week
			}
		});
 
	}
});
 
Ext.onReady(function(){
	Ext.create("CSE330.Calendar");
});