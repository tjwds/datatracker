from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from functools import wraps

from ietf.ietfauth.decorators import has_role

def check_for_cancel(redirect_url):
    """
    Decorator to make a view redirect to the given url if the reuqest is a POST which contains
    a submit=Cancel.
    """
    #assert False, redirect_url
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method == 'POST' and request.POST.get('submit',None) == 'Cancel':
                return HttpResponseRedirect(redirect_url)
            return func(request, *args, **kwargs)
        return inner
    return decorator
    
def check_permissions(func):
    """
    This decorator checks that the user making the request has access to the
    object being requested.  Expects one of the following four keyword
    arguments: group_id, meeting_id, slide_id, session_id.  
    """
    def wrapper(request, *args, **kwargs):
        # short circuit.  secretariat user has full access
        if has_role(request.user,'Secretariat'):
            return func(request, *args, **kwargs)
        
        #TODO delete this
        return func(request, *args, **kwargs)
        '''
        # get the parent group
        if 'group_id' in kwargs:
            group_id = kwargs['group_id']
        elif 'meeting_id' in kwargs:
            meeting = Meeting.objects.get(id=kwargs['meeting_id'])
            group_id = meeting.group
        elif 'slide_id' in kwargs:
            slide = InterimFile.objects.get(id=kwargs['slide_id'])
            group_id = slide.meeting.group_acronym_id
        elif 'session_id' in kwargs:
            session = get_object_or_404(WgMeetingSession, session_id=kwargs['session_id'])
            group_id = session.group_acronym_id
            
        if has_role(request.user,'Area Director'):
            ad = AreaDirector.objects.get(person=request.person)
            ags = AreaGroup.objects.filter(area=ad.area)
            if ags.filter(group=group_id):
                return func(request, *args, **kwargs)
        else:
            if ( WGChair.objects.filter(group_acronym=group_id,person=request.person) or
            WGSecretary.objects.filter(group_acronym=group_id,person=request.person) or
            IRTFChair.objects.filter(irtf=group_id,person=request.person)):
                return func(request, *args, **kwargs)
 
        if request.user_is_ietf_iab_chair and group_id in ('-1','-2'):
            return func(request, *args, **kwargs)
            
        # if we get here access is denied
        group = get_group_or_404(group_id)
        return render_to_response('unauthorized.html',{
            'user_name':request.person,
            'group_name':str(group)}
        )
        '''
    return wraps(func)(wrapper)
