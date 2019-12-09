def K(self, basis):
        '''Initializer which find all small sector based on translational invarient.'''
        #get infomation of target basis
        st = basis.state
        symmetry = basis.symmetry.copy()
        print("Initializing momentum sectors of given basis : ({},{},{},{})\t\t\t\t".format(*symmetry),end = '\r')
        #make new empty storage
        state, address, period, distance, counts = [],[],[],[],[]# [[] for q in range(self.size+1)],[[] for q in range(self.size+1)],[[] for q in range(self.size+1)],[[] for q in range(self.size+1)]
        states = {}
        for k in range(self.system.size):
            state.append([])
            address.append({})
            period.append([])
            distance.append({s:0 for s in st})
            counts.append(0)


        #calculate period of each state based on traslation op
        pe = self._ncheck(st, self.system.size) ## calculate state if st is not rep. state return -1, else return period
        dist = {}
        St = st
        stpr = {}

        for s,p in zip(st,pe):
            stpr[s] = p  #get period from state
            for k in range(self.system.size):
                if p<0:
                    continue
                    print(s, p)
                    address[k][s] = address[k][self._rtranslate(s)]
                #debug
                elif p ==0:
                    raise ValueError("something wrong when state ({}) got period 0.".format(s))
                if k*p % self.system.size == 0:
                    state[k].append(s)
                    if k == 0: states[s] = [s]
                    address[k][s] = counts[k]
                    ts = s
                    for l in range(p-1):
                        ts = self._rtranslate(ts)
                        if k == 0: states[s].append(ts)
                        address[k][ts] = counts[k]
                        distance[k][ts] = l+1
                    period[k].append(p)
                    counts[k] += 1
        l = len(state[0])
        kstate = -1*np.ones([l,self.system.size+1],dtype = np.int64)
        i=0
        for key, val in list(states.items()):
            kstate[i,0] = key
            assert len(val) == period[0][address[0][key]]
            for j,value in enumerate(val):
                kstate[i,j+1] = value
            i+=1
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
            folder.create_dataset('address',data = np.array(list(address[k].items())),compression = 'lzf')
            folder.create_dataset('period',data = np.array(period[k]),compression = 'lzf')
            if k ==0 :
                folder.create_dataset('distance',data = np.array(list(distance[k].items())),compression = 'lzf')
                folder.create_dataset('state_set',data = kstate,compression = 'lzf')
                ks = folder['state_set']
                ds = folder['distance']
            else:
                folder['state_set'] = ks
                folder['distance'] = ds
            folder.attrs['counts'] = counts[k]
