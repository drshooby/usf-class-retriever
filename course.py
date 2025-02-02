class Course:
    def __init__(self,
                 subject,
                 course_title,
                 course_number,
                 prof_name,
                 prof_email,
                 term,
                 building,
                 room,
                 days,
                 meeting_type,
                 start_time,
                 end_time):
        self.subject = subject
        self.course_title = course_title
        self.course_number = course_number
        self.prof_name = prof_name
        self.prof_email = prof_email
        self.term = term
        self.building = building
        self.room = room
        self.days = days
        self.meeting_type = meeting_type

        def twenty_four_to_twelve(time):
            if not time:
                return "N/A"
            hour = int(time[:2])
            if hour > 12:
                return str(hour - 12) + ":" + time[2:] + "PM"
            time_str = str(hour) + ":" + time[2:]
            if hour == 12:
                return time_str + "PM"
            return time_str + "AM"

        self.start_time = twenty_four_to_twelve(start_time)
        self.end_time = twenty_four_to_twelve(end_time)

    def __str__(self):
        return f'''
            Subject: {self.subject}
            Course Title: {self.course_title}
            Course Number: {self.course_number}
            Professor Name: {self.prof_name}
            Professor Email: {self.prof_email}
            Term: {self.term}
            Building: {self.building}
            Room: {self.room}
            Days: {self.days}
            Meeting Type: {self.meeting_type}
            Start Time: {self.start_time}
            End Time: {self.end_time}
        '''