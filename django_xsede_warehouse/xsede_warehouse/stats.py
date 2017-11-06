from datetime import datetime

# The following class is under development and may replace StatsSummary
class StatsTracker():
    def __init__(self, Label, StatTypes):
        self.Label = Label
#        self.ServiceSource = Source
        self.ProcessingSeconds = 0
        self.StartAt = datetime.now()
        self.stats = {}
        if type(StatTypes) is list:
            self.StatTypes = StatTypes
        else:
            self.StatTypes = []
            self.StatTypes.append(StatTypes)
        for t in self.StatTypes:
            self.stats['%s.Current' % t] = 0
            self.stats['%s.New' % t] = 0
            self.stats['%s.Updates' % t] = 0
            self.stats['%s.Deletes' % t] = 0
            self.stats['%s.ToCache' % t] = 0
        
    def __unicode__(self):
        return(self.summary())
    def set(self, key, value):
#        if key in self.stats:
        self.stats[key] = value
    def add(self, key, increment):
        if key in self.stats:
            self.stats[key] += increment
    def end(self):
        self.ProcessingSeconds = datetime.now() - self.StartAt
    def summary(self):
        out = 'Processed %s in %s/sec:' % (self.Label, str(self.ProcessingSeconds))
        for i in self.StatTypes:
            if '%s.New' % i in self.stats and self.stats['%s.New' % i] > 0:
                out += ' %s %s->%s (%s/up' % (i, self.stats['%s.Current' % i], self.stats['%s.New' % i], self.stats['%s.Updates' % i])
                if '%s.Deletes' % i in self.stats and self.stats['%s.Deletes' % i] > 0:
                    out += ', %s/del' % self.stats['%s.Deletes' % i]
                if '%s.ToCache' % i in self.stats and self.stats['%s.ToCache' % i] > 0:
                    out += ', %s/cache' % self.stats['%s.ToCache' % i]
                out += ')'
        return(out)
