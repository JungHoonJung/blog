def K(self, basis):
        '''Initializer which find all small sector based on translational invarient.'''
        #get infomation of target basis
        st = basis.state
        symmetry = basis.symmetry.copy()
        logger = self.logger.getChild('K')
        logger.info("Initializing momentum sectors of given basis : ({},{},{},{})\t\t\t\t".format(*symmetry))
        #make new empty storage
        state, address, period, distance, counts = [],[],{},{s:-1 for s in st},[]# [[] for q in range(self.size+1)],[[] for q in range(self.size+1)],[[] for q in range(self.size+1)],[[] for q in range(self.size+1)]
        states = {}
        for k in range(self.system.size):
            state.append([])
            address.append({})
            #period.append([])
            counts.append(0)


        #calculate period of each state based on traslation op
        pe = self._ncheck(st, self.system.size) ## calculate state if st is not rep. state return -1, else return period
        dist = {}
        St = st
        stpr = {}

        for s,p in zip(st,pe):
            stpr[s] = p  #get period from state
            if p<0:
                if not distance.get(s,False):
                    logger.critical("State('{}') which is not included traslational symmetry is founded.".format(s))
                continue
                print(s, p)
                address[k][s] = address[k][self._rtranslate(s)] #acsending order. so, the bigger one comes later.

            #debug
            elif p ==0:
                raise ValueError("something wrong with state ({}) got period 0.".format(s))
            else:
                #make representative state that is consist of states.
                logger.debug("State '{}' is selected as representative state(RS) with period '{}'.".format(s, p))
                states[s] = [s]                  #state_set (set of states which matched with translational symmetry)
                period[s] = p
                ts = s
                distance[s] = 0
                for l in range(p-1):
                    ts = self._rtranslate(ts) #bit shift to left periodically
                    logger.debug("\tT^{:>2} |{}> : {}  ({:>2}).".format(l+1, self.binary(s), self.binary(ts),ts))
                    states[s].append(ts)
                    distance[ts] = l+1
                logger.debug("All members of RS '{}' is founded.")
            logger.debug("And RS '{}' is belonging to".format(s))
            for k in range(self.system.size):
                if k*p % self.system.size == 0:
                    state[k].append(s)
                    logger.debug("\tk = {:>2} momentum sector.".format(k, s, p))
                    #address[k][s] = counts[k]
                    #period[k].append(p)
                    counts[k] += 1
        l = len(state[0])
        kstate = -1*np.ones([l,self.system.size+1],dtype = np.int64)
        i=0
        for key, val in list(states.items()):
            kstate[i,0] = key
            assert len(val) == period[key]
            for j,value in enumerate(val):
                kstate[i,j+1] = value
            i+=1
        for key in distance:
            if distance[key] == -1:
                logger.critical("State '' still has negative distance(assertion).")
                assert distance[key] != -1, "state '' is not considered.".format(key)


        #deprecated code
        '''dist = {}
        adrs = {}
        state_to_period = lambda x: stpr.get(x)
        state_to_period = np.vectorize(state_to_period)
        for d in range(self.system.size):
            ch = state_to_period(St)
            for chs,chks in zip(st[np.logical_not(ch==-1)],St[np.logical_not(ch==-1)]):
                dist[chs] = d
                adrs[chs] = address[0][chks]
                assert d<state_to_period(chks),"d {},pe {}".format(d, state_to_period(chks))
            St = St[ch ==-1]
            if len(St) == 0 : break
            st = st[ch ==-1]
            St = self.translate(St)

        for k in range(self.system.size):
            for s in state[k]:
                if address[k].get(s,None) is None:
                    address[k][s] = adrs[s]
                    distance[k][s] = dist[s]'''

        bsaver = self.system.saver.file.require_group('/basis')
        for k in range(self.system.size):
            assert len(state[k]) == counts[k], 'component and its label unmatched'
            symmetry[1] = k
            folder = bsaver.require_group('({},{},{},{})'.format(*symmetry))
            folder.create_dataset('state',data = np.array(state[k]),compression = 'lzf')
            #folder.create_dataset('address',data = np.array(list(address[k].items())),compression = 'lzf')

            logger.debug("'{}' created, and 'state', 'period', 'distance', 'state_set' are added".format(symmetry))
            if k ==0 :
                folder.create_dataset('period',data = np.array(list(period.items())),compression = 'lzf')
                folder.create_dataset('distance',data = np.array(list(distance.items())),compression = 'lzf')
                folder.create_dataset('state_set',data = kstate,compression = 'lzf')
                ks = folder['state_set']
                ds = folder['distance']
                peri = folder['period']
            else:
                folder['state_set'] = ks
                folder['distance'] = ds
                folder['period'] = peri
            folder.attrs['counts'] = counts[k]
        logger.info("Calculation ended for basis : {}".format(basis.symmetry.copy()))
        del logger
