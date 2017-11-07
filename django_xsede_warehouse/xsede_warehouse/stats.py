from datetime import datetime

# The following class is under development and may replace StatsSummary
class StatsTracker():
    def __init__(self, Label, StatTypes):
        self.Label = Label
        self.ProcessingSeconds = 0
        self.StartTS = datetime.now()
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
        self.stats[key] = value
    def add(self, key, increment):
        if key in self.stats:
            self.stats[key] += increment
    def end(self):
        self.ProcessingSeconds = datetime.now() - self.StartTS
    def summary(self):
        out = 'Processed %s in %s/sec:' % (self.Label, self.ProcessingSeconds.total_seconds())
        for i in self.StatTypes:
            if self.stats.get('%s.New' % i, None) > 0:
                out += ' %s %s->%s (%s/up' % (i, self.stats['%s.Current' % i], self.stats['%s.New' % i], self.stats['%s.Updates' % i])
                if self.stats.get('%s.Deletes' % i, None) > 0:
                    out += ', %s/del' % self.stats['%s.Deletes' % i]
                if self.stats.get('%s.ToCache' % i, None) > 0:
                    out += ', %s/cache' % self.stats['%s.ToCache' % i]
                out += ')'
        return(out)
