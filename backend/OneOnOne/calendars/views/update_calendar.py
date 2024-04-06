from calendars.models.calendar import Calendar
from calendars.models.timeblock import TimeBlock
from calendars.models.event import Event
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class CalendarUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request, format=None):
        # all accepted fields
        fields = ['event_id', 'yr', 'wk', 'day', 'time', 'pref']

        nullable_field_combos = [
            # Permanent change of preference 
            # - Time block becomes unavailable if pref is null
            ['event_id', 'yr', 'wk', 'pref'],
            # - Permanent change to the user's preference for that time block
            ['event_id', 'yr', 'wk'],
            # Temporary change of preference
            ['event_id'],
            # Delete the temporary change of preference
            ['event_id', 'pref'],
            # an event takes place
            ['pref']
        ]
        
        unspecified_fields = []
        
        # Collect all null/unspecified fields
        for field in fields:
            if (
                field not in request.data
                or request.data[field] == ''
                or request.data[field] is None
            ):
                unspecified_fields.append(field)
        
        # Only allow a max of 2 fields being null/unspecified
        if len(unspecified_fields) > 4:
            return Response(
                data={'error': f'missing too many fields. {unspecified_fields} are currently null/unspecified'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if the null/unspecified fields are in the allowed combo list
        if (
            unspecified_fields not in nullable_field_combos 
            and len(unspecified_fields) != 0
        ):
            return Response(
                data={'error':f'null/unspecified field combination not accepted. Accepted combos: {nullable_field_combos[0]}, {nullable_field_combos[1]}, and {nullable_field_combos[2]}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for data type of fields
        for field in list(set(fields) - set(unspecified_fields)):
            try:
                if field == "time": 
                    float(request.data[field])
                else:
                    int(request.data[field])
            except ValueError as e:
                return Response(
                    data={'error':f'incorrect data type for {field}: {str(e)}'}
                )
        
        user_calendar = Calendar.objects.get(owner=request.user.id)
        
        # Some data validation tasks
        day = int(request.data['day'])
        if day < 0 or day > 7:
            return Response(
                data={'error':f'invalid day: {day}th day of week doesn\'t exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        time = float(request.data['time'])
        if time < 0 or time > 23.5:
            return Response(
                data={'error':f'invalid time: hour {time} doesn\'t exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check the value of pref
        if (
            'pref' not in request.data
            or request.data['pref'] == "" 
            or request.data['pref'] is None 
        ):
            pref = None
        # Update the time block's preference
        else:
            pref = int(request.data['pref'])
            if pref not in [1,2]:
                return Response(
                    data={'error':f'invalid preference: {pref} is not in the accepted values [1, 2]'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Temporary change of preference for a time block
        handler_type = nullable_field_combos.index(unspecified_fields)
        if (handler_type == 0 or handler_type == 1):
            return self.permanent_change(request, user_calendar, day, time, pref)
        elif (handler_type == 2 or handler_type == 3):
            return self.temporary_change(request, user_calendar, day, time, pref)
        else:
            return self.event_occurs(request, user_calendar, day, time)
    
    def permanent_change(self, request, cal: Calendar, day: int, time: int, pref) -> Response:        
        # If the time block exists
        if TimeBlock.objects.filter(day=day, time=time, calendar=cal.id).exists():
            timeblock = TimeBlock.objects.get(
                calendar=cal,
                day=day,
                time=time
            )
            # Make the time block unavailable
            if pref is None:
                timeblock.delete()
            # Update the time block's preference
            else:
                timeblock.preference = pref
                timeblock.save()
            
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            if (
                'pref' not in request.data
                or request.data['pref'] == "" 
                or request.data['pref'] is None
            ):
                return Response(
                    data={'error':'cannot delete nonexistent time block: user is already unavaiable at that time block'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            new_timeblock = TimeBlock()
            new_timeblock.calendar = cal
            new_timeblock.day = day
            new_timeblock.time = time
            new_timeblock.preference = int(request.data['pref'])
            new_timeblock.save()
            
            return Response(status=status.HTTP_201_CREATED)
        
    def temporary_change(self, request, cal, day, time, pref):
        yr = int(request.data['yr'])
        wk = int(request.data['wk'])
        if wk < 0 or wk > 52:
            return Response(
                data={'error':f'invalid week numberL: there is no {wk}th week'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the time block exists
        exists = TimeBlock.objects.filter(calendar=cal.id, yr=yr, wk=wk, day=day, time=time).exists()
        
        # If the time block exists and pref is null, then it means that the user wants to delete this temp block
        if exists and pref is None:
            timeblock = TimeBlock.objects.get(calendar=cal.id, yr=yr, wk=wk, day=day, time=time)
            timeblock.delete()
            return Response(status=status.HTTP_200_OK)
        # If just exists with a new preference, we will just get the timeblock and update it accordingly
        elif exists:
            timeblock = TimeBlock.objects.get(calendar=cal.id, yr=yr, wk=wk, day=day, time=time)
        else:
            timeblock = TimeBlock()
            timeblock.calendar = cal
            timeblock.yr = yr
            timeblock.wk = wk
            timeblock.day = day
            timeblock.time = time
        
        timeblock.pref = pref
        timeblock.save()
        
        return Response(status=status.HTTP_200_OK)
    
    def event_occurs(self, request, cal, day, time):
        yr = int(request.data['yr'])
        wk = int(request.data['wk'])
        event_id = int(request.data['event_id'])
        
        # Check if the time block for the event is already created
        new_timeblock = False
        try:
            timeblock = TimeBlock.objects.get(calendar=cal, event=event_id)
        except ObjectDoesNotExist:
            timeblock = TimeBlock()
            new_timeblock = True

        # If it's a new time block but the event also doesn't exist, return 400
        if not Event.objects.filter(pk=event_id).exists() and new_timeblock:
            return Response(
                data={'error':f'invalid event: event {event_id} doesn\'t exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_timeblock:    
            # The time block needs to be created
            timeblock.calendar = cal
            timeblock.event = Event.objects.get(pk=event_id, owner=request.user.id)
            
        # This is the case where the event is newly created or has been modified
        # we will update the timeblock with the new/updated information
        timeblock.time = time
        timeblock.yr = yr
        timeblock.wk = wk
        timeblock.day = day
        timeblock.save()
        
        return Response(
            status=status.HTTP_200_OK
        )
        