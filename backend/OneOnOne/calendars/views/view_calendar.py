from calendars.models.calendar import Calendar
from calendars.models.timeblock import TimeBlock
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from calendars.models.serializers import TimeBlockSerializer

class CalendarView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get(self, request, format=None, **kwargs) -> Response:
        calendar = Calendar.objects.get(owner=request.user.id)
        yr = int(kwargs['yr'])
        wk = int(kwargs['wk'])
        if wk > 52:
            return Response(
                    data={'error':f'invalid week number: there is no {wk}th{" (nice) " if wk==69 else " "}week of the year'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        start_dt, end_dt = self.get_wk_date_range(yr, wk)
        
        # First get all the default preferences
        default_blocks = TimeBlock.objects.filter(
            calendar=calendar.id,
            event__isnull=True, time__isnull=False, yr__isnull=True, 
            wk__isnull=True, day__isnull=False, preference__isnull=False
        ).all()
        
        # Get all the event blocks
        event_blocks = TimeBlock.objects.filter(
            calendar=calendar.id,
            event__isnull=False, time__isnull=False, yr__isnull=False, 
            wk__isnull=False, day__isnull=False, preference__isnull=True
        ).filter(calendar=calendar.id, yr=yr, wk=wk).all()
        
        # Get all temporary blocks
        # if event is null and everything is not, then it's a temp change in pref
        # if event and pref are both null, then it's temp unavailable at that time
        temp_blocks = TimeBlock.objects.filter(
            calendar=calendar.id,
            event__isnull=True, time__isnull=False, yr__isnull=False, 
            wk__isnull=False, day__isnull=False
        ).filter(calendar=calendar.id, yr=yr, wk=wk).all()
        
        timeblocks = []
        
        # As events has the highest priority, this will be added first
        for event in event_blocks:
            timeblocks.append(dict(TimeBlockSerializer(event).data))

        # Then the temp events
        if len(timeblocks) == 0:
            for temp_block in temp_blocks:
                timeblocks.append(dict(TimeBlockSerializer(temp_block).data))
        else:
            for temp_block in temp_blocks:
                found = False
                for block in timeblocks:
                    if ((block['day'] == temp_block.day and block['time'] == temp_block.time)
                        or block['id'] == temp_block.pk
                    ):
                        found = True
                if not found:
                    timeblocks.append(dict(TimeBlockSerializer(temp_block).data))
        
        # Finally the default preferences
        if len(timeblocks) == 0:
            for d_block in default_blocks:
                timeblocks.append(dict(TimeBlockSerializer(d_block).data))
        else:
            for d_block in default_blocks:
                found = False
                for block in timeblocks:
                    if ((block['day'] == d_block.day and block['time'] == d_block.time)
                        or block['id'] == d_block.pk
                    ):
                        found = True
                if not found:
                    timeblocks.append(dict(TimeBlockSerializer(d_block).data))
        
        json_data = {
            'id': calendar.id,
            'start_dt': str(start_dt.date()),
            'end_dt': str(end_dt.date()),
            'yr': yr,
            'wk': wk,
            'timeblocks': timeblocks
        }
               
        return Response(
            data=json_data    
        )
            
    def get_wk_date_range(self, yr: int, wk: int):
        # We are using Monday as the 1st day of week here
        # Begin from the first day of the year
        start_date = datetime(year=yr, month=1, day=1)
        
        days_from_monday = start_date.weekday()
        
        # avoid double counting week 1
        start_date += timedelta(weeks=wk-1)
        # revert the date back to Monday
        start_date -= timedelta(days_from_monday)
        
        # Increment by 6 days to get end of week
        end_date = start_date + timedelta(days=6)
        
        return start_date, end_date
        
        